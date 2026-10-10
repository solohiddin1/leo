import json

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime

from apps.order.models import Cart, CartItem, Order, OrderItem
from apps.order.repositories.cart_repo import CartRepo
from apps.product.models import Category, Image, Product, SubCategory
from apps.shared.models import Region, Store
from apps.transaction.models import Bonus, BonusClaimStatus, BonusCode, UserSumma
from apps.user.models import User

# usta-source's user.Region.pk -> leo's shared.Region.soato_id, matched by hand against
# apps/shared/regions.json (usta only has 12 of Uzbekistan's 14 regions; it has no rows
# for Tashkent viloyati or Qoraqalpog'iston, so those are simply never referenced below).
REGION_SOATO_BY_USTA_PK = {
    1: 1726,  # Toshkent shahri
    2: 1703,  # Andijon viloyati
    3: 1706,  # Buxoro viloyati
    4: 1708,  # Jizzax viloyati
    6: 1710,  # Qashqadaryo viloyati
    7: 1712,  # Navoiy viloyati
    8: 1714,  # Namangan viloyati
    9: 1718,  # Samarqand viloyati
    10: 1724,  # Sirdaryo viloyati
    11: 1722,  # Surxondaryo viloyati
    12: 1730,  # Farg'ona viloyati
    13: 1733,  # Xorazm viloyati
}


class _DryRunRollback(Exception):
    pass


def _index_by_model(rows):
    by_model = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)
    return by_model


def _force_created_at(instance, created_at):
    if created_at:
        type(instance).objects.filter(pk=instance.pk).update(created_at=created_at)


class Command(BaseCommand):
    help = (
        "One-time import of a usta-source `dumpdata user product` JSON into leo. "
        "Safe to re-run: every step is get_or_create'd on a natural key. "
        "Media files (category/product/store icons) are NOT copied by this command — "
        "rsync usta-source's media/ into leo's media/ first, the relative paths match."
    )

    def add_arguments(self, parser):
        parser.add_argument("dump_path", help="Path to the usta-source dumpdata JSON file")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the whole import inside a transaction that is rolled back at the end",
        )

    def handle(self, *args, **options):
        with open(options["dump_path"], encoding="utf-8") as f:
            rows = json.load(f)
        by_model = _index_by_model(rows)
        self.counts = {}

        try:
            with transaction.atomic():
                region_map = self._migrate_regions(by_model.get("user.region", []))
                store_map = self._migrate_stores(
                    by_model.get("user.store", []),
                    by_model.get("user.storephone", []),
                    region_map,
                )
                category_map = self._migrate_categories(by_model.get("product.category", []))
                subcategory_map = self._migrate_subcategories(
                    by_model.get("product.subcategory", []), category_map
                )
                product_map = self._migrate_products(
                    by_model.get("product.product", []), subcategory_map
                )
                self._migrate_product_images(
                    by_model.get("product.productimage", []), product_map
                )
                user_map = self._migrate_users(
                    by_model.get("user.telegramuser", []), region_map
                )
                bonus_map, bonus_code_map = self._migrate_bonuses(
                    by_model.get("product.bonus", []),
                    by_model.get("product.usersumma", []),
                    product_map,
                )
                self._migrate_user_summas(
                    by_model.get("product.usersumma", []),
                    user_map,
                    bonus_map,
                    bonus_code_map,
                )
                order_map = self._migrate_orders(
                    by_model.get("product.order", []), user_map, store_map
                )
                self._migrate_order_items(
                    by_model.get("product.orderproduct", []), order_map, product_map
                )
                self._migrate_carts(
                    by_model.get("product.cart", []), user_map, product_map
                )

                self.stdout.write(self.style.SUCCESS("Import summary:"))
                for key, value in self.counts.items():
                    self.stdout.write(f"  {key}: {value}")

                if options["dry_run"]:
                    self.stdout.write(self.style.WARNING("--dry-run: rolling back."))
                    raise _DryRunRollback
        except _DryRunRollback:
            pass

    def _count(self, key, n=1):
        self.counts[key] = self.counts.get(key, 0) + n

    # -- regions / stores ---------------------------------------------------

    def _migrate_regions(self, region_rows):
        region_map = {}
        for row in region_rows:
            soato_id = REGION_SOATO_BY_USTA_PK.get(row["pk"])
            if not soato_id:
                self.stdout.write(
                    self.style.WARNING(
                        f"user.Region pk={row['pk']} ({row['fields']['name']}) has no "
                        "known soato_id mapping — skipped"
                    )
                )
                continue
            region = Region.objects.filter(soato_id=soato_id).first()
            if not region:
                self.stdout.write(
                    self.style.WARNING(
                        f"leo has no seeded Region for soato_id={soato_id} — skipped. "
                        "Load apps/shared/regions.json first."
                    )
                )
                continue
            region_map[row["pk"]] = region.id
            self._count("regions.matched")
        return region_map

    def _migrate_stores(self, store_rows, phone_rows, region_map):
        phones_by_store = {}
        for row in phone_rows:
            phones_by_store.setdefault(row["fields"]["store"], []).append(
                row["fields"]["phone"]
            )

        store_map = {}
        for row in store_rows:
            fields = row["fields"]
            region_id = region_map.get(fields["region"])
            store, created = Store.objects.get_or_create(
                name=fields["name"],
                region_id=region_id,
                defaults={
                    "phone_number": (phones_by_store.get(row["pk"]) or [""])[0],
                    "lat": fields["latitude"] or None,
                    "long": fields["longitude"] or None,
                },
            )
            store_map[row["pk"]] = store.id
            self._count("stores.created" if created else "stores.matched")
        return store_map

    # -- catalog --------------------------------------------------------------

    def _migrate_categories(self, category_rows):
        category_map = {}
        for row in category_rows:
            fields = row["fields"]
            name_uz = fields.get("name_uz") or fields.get("name") or ""
            name_ru = fields.get("name_ru") or fields.get("name") or ""

            category = Category.objects.filter(name=fields["name"]).first()
            if not category:
                category = Category.objects.filter(name_uz=name_uz).first()
            if not category:
                category = Category.objects.filter(name_ru=name_ru).first()

            if not category:
                category = Category(
                    name=fields["name"],
                    name_uz=name_uz,
                    name_ru=name_ru,
                    image=fields.get("icon") or "",
                )
                category.save()
                created = True
            else:
                created = False
                category.name = fields["name"]
                category.name_uz = name_uz
                category.name_ru = name_ru
                if fields.get("icon"):
                    category.image = fields.get("icon")
                category.save(update_fields=["name_uz", "name_ru", "image"])

            category_map[row["pk"]] = category.id
            self._count("categories.created" if created else "categories.matched")
        return category_map

    def _migrate_subcategories(self, subcategory_rows, category_map):
        subcategory_map = {}
        # Two passes: usta's `parent` FK can point at another SubCategory, so create
        # everything first, then wire up `parent` once every id is known.
        pending_parents = {}
        for row in subcategory_rows:
            fields = row["fields"]
            name_uz = fields.get("name_uz") or fields.get("name") or ""
            name_ru = fields.get("name_ru") or fields.get("name") or ""
            cat_id = category_map.get(fields["category"])

            subcategory = SubCategory.objects.filter(name=fields["name"], category_id=cat_id).first()
            if not subcategory:
                subcategory = SubCategory.objects.filter(name_uz=name_uz, category_id=cat_id).first()
            if not subcategory:
                subcategory = SubCategory.objects.filter(name_ru=name_ru, category_id=cat_id).first()

            if not subcategory:
                subcategory = SubCategory(
                    name=fields["name"],
                    name_uz=name_uz,
                    name_ru=name_ru,
                    category_id=cat_id,
                    image=fields.get("icon") or "",
                )
                subcategory.save()
                created = True
            else:
                created = False
                subcategory.name = fields["name"]
                subcategory.name_uz = name_uz
                subcategory.name_ru = name_ru
                if fields.get("icon"):
                    subcategory.image = fields.get("icon")
                subcategory.save(update_fields=["name_uz", "name_ru", "image"])

            subcategory_map[row["pk"]] = subcategory.id
            self._count("subcategories.created" if created else "subcategories.matched")
            if fields.get("parent"):
                pending_parents[subcategory.id] = fields["parent"]

        for subcategory_id, usta_parent_pk in pending_parents.items():
            parent_id = subcategory_map.get(usta_parent_pk)
            if parent_id:
                SubCategory.objects.filter(pk=subcategory_id).update(parent_id=parent_id)
        return subcategory_map

    def _migrate_products(self, product_rows, subcategory_map):
        product_map = {}
        for row in product_rows:
            fields = row["fields"]
            name_uz = fields.get("name_uz") or fields.get("name") or ""
            name_ru = fields.get("name_ru") or fields.get("name") or ""
            desc_uz = fields.get("description_uz") or fields.get("description") or ""
            desc_ru = fields.get("description_ru") or fields.get("description") or ""
            subcat_id = subcategory_map.get(fields["category"])

            product = Product.objects.filter(name=fields["name"], category_id=subcat_id).first()
            if not product:
                product = Product.objects.filter(name_uz=name_uz, category_id=subcat_id).first()
            if not product:
                product = Product.objects.filter(name_ru=name_ru, category_id=subcat_id).first()

            if not product:
                product = Product(
                    name=fields["name"],
                    name_uz=name_uz,
                    name_ru=name_ru,
                    description=desc_uz,
                    description_uz=desc_uz,
                    description_ru=desc_ru,
                    price=fields["price"],
                    ordering=fields.get("order", 0),
                    is_active=True,
                    category_id=subcat_id,
                )
                product.save()
                created = True
            else:
                created = False
                product.name = fields["name"]
                product.name_uz = name_uz
                product.name_ru = name_ru
                product.description = desc_uz
                product.description_uz = desc_uz
                product.description_ru = desc_ru
                product.price = fields["price"]
                product.ordering = fields.get("order", 0)
                product.save(update_fields=[
                    "name_uz", "name_ru", "description", "description_uz", "description_ru", "price", "ordering"
                ])

            product_map[row["pk"]] = product.id
            self._count("products.created" if created else "products.matched")
        return product_map

    def _migrate_product_images(self, image_rows, product_map):
        for row in image_rows:
            fields = row["fields"]
            product_id = product_map.get(fields["product"])
            if not product_id:
                continue
            _, created = Image.objects.get_or_create(
                product_id=product_id, image=fields["image"]
            )
            self._count("product_images.created" if created else "product_images.matched")

    # -- users ------------------------------------------------------------------

    def _migrate_users(self, telegram_user_rows, region_map):
        user_map = {}
        taken_usernames = set(User.objects.values_list("username", flat=True))

        for row in telegram_user_rows:
            fields = row["fields"]
            chat_id = fields["chat_id"]

            existing = User.objects.filter(telegram_id=str(chat_id)).first()
            if existing:
                user_map[row["pk"]] = existing.id
                self._count("users.matched")
                continue

            username = fields.get("phone") or f"tg_{chat_id}"
            if username in taken_usernames:
                username = f"{username}_{chat_id}"
            taken_usernames.add(username)

            lang = fields.get("lang") if fields.get("lang") in ("uz", "ru") else "uz"

            user = User(
                username=username,
                first_name=fields.get("name") or "",
                telegram_id=str(chat_id),
                lang=lang,
                balance=fields.get("summa", 0),
                is_verified=True,
                region_id=region_map.get(fields.get("region")),
            )
            user.set_unusable_password()
            user.save()
            _force_created_at(user, fields.get("created_at"))
            CartRepo.get_or_create_cart(user)

            user_map[row["pk"]] = user.id
            self._count("users.created")
        return user_map

    # -- bonus codes --------------------------------------------------------

    def _migrate_bonuses(self, bonus_rows, user_summa_rows, product_map):
        bonus_map = {}
        bonus_code_map = {}
        for row in bonus_rows:
            fields = row["fields"]
            product_id = product_map.get(fields["product"])

            existing_code = BonusCode.objects.filter(code=fields["code"]).first()
            if existing_code:
                bonus_map[row["pk"]] = existing_code.bonus_id
                bonus_code_map[row["pk"]] = existing_code.id
                if existing_code.bonus and not existing_code.bonus.prefix:
                    existing_code.bonus.prefix = fields["code"]
                    existing_code.bonus.save(update_fields=["prefix"])
                self._count("bonus_codes.matched")
                continue

            bonus = Bonus.objects.create(
                product_id=product_id,
                summa=fields["summa"],
                prefix=fields["code"],
                quantity=10000,
            )
            bonus_code = BonusCode.objects.filter(bonus=bonus, code=fields["code"]).first()
            bonus_map[row["pk"]] = bonus.id
            if bonus_code:
                bonus_code_map[row["pk"]] = bonus_code.id
            self._count("bonus_codes.created")
        return bonus_map, bonus_code_map

    def _migrate_user_summas(self, user_summa_rows, user_map, bonus_map, bonus_code_map):
        rows_sorted = sorted(
            user_summa_rows, key=lambda r: (r["fields"].get("created_at") or "", r["pk"])
        )

        used_code_ids = set()

        for row in rows_sorted:
            fields = row["fields"]
            user_id = user_map.get(fields["user"])
            if not user_id:
                self._count("user_summas.skipped_no_user")
                continue

            raw_code = fields["code"]
            usta_bonus_pk = fields.get("bonus")
            bonus_id = bonus_map.get(usta_bonus_pk) if usta_bonus_pk else None
            product_id = (
                Bonus.objects.filter(pk=bonus_id).values_list("product_id", flat=True).first()
                if bonus_id
                else None
            )

            # Check if there is an existing legacy #usta placeholder from a previous migration run
            old_placeholder_code = f"{raw_code}#usta{row['pk']}"
            old_placeholder = BonusCode.objects.filter(code=old_placeholder_code).first()

            # Find or get the real BonusCode
            bonus_code = BonusCode.objects.filter(code=raw_code).first()

            if not bonus_code:
                # If the code was not in the generated batch, create it with its real bonus
                bonus_obj = Bonus.objects.filter(pk=bonus_id).first() if bonus_id else None
                bonus_code, _ = BonusCode.objects.get_or_create(
                    code=raw_code,
                    defaults={"bonus": bonus_obj, "is_used": True},
                )
            elif bonus_id and not bonus_code.bonus_id:
                bonus_code.bonus_id = bonus_id
                bonus_code.save(update_fields=["bonus_id"])

            if not product_id and bonus_code.bonus and bonus_code.bonus.product_id:
                product_id = bonus_code.bonus.product_id

            # Ensure is_used is set
            if not bonus_code.is_used:
                bonus_code.is_used = True
                bonus_code.save(update_fields=["is_used"])

            # Handle duplicate usage (rare cases like AVP4A0000 where the same code was used multiple times)
            if bonus_code.id in used_code_ids or (
                UserSumma.objects.filter(code_id=bonus_code.id)
                .exclude(user_id=user_id, summa=fields["summa"])
                .exists()
            ):
                duplicate_code = f"{raw_code}#dup{row['pk']}"
                target_code, _ = BonusCode.objects.get_or_create(
                    code=duplicate_code,
                    defaults={"bonus": bonus_code.bonus, "is_used": True},
                )
            else:
                target_code = bonus_code
                used_code_ids.add(bonus_code.id)

            # If an old #usta placeholder exists, migrate the existing UserSumma record to target_code
            if old_placeholder:
                existing_claim = UserSumma.objects.filter(code_id=old_placeholder.id).first()
                if existing_claim:
                    existing_claim.code = target_code
                    if bonus_id:
                        existing_claim.bonus_id = bonus_id
                    if product_id:
                        existing_claim.product_id = product_id
                    existing_claim.save(update_fields=["code", "bonus", "product"])
                    old_placeholder.delete()
                    self._count("user_summas.matched")
                    continue

            user_summa, created = UserSumma.objects.get_or_create(
                code_id=target_code.id,
                defaults=dict(
                    user_id=user_id,
                    bonus_id=bonus_id or target_code.bonus_id,
                    store=None,
                    product_id=product_id,
                    summa=fields["summa"],
                    status=BonusClaimStatus.APPROVED,
                    is_expired=fields.get("is_expired", False),
                ),
            )
            if created:
                _force_created_at(user_summa, fields.get("created_at"))
                self._count("user_summas.created")
            else:
                update_fields = []
                if (bonus_id or target_code.bonus_id) and not user_summa.bonus_id:
                    user_summa.bonus_id = bonus_id or target_code.bonus_id
                    update_fields.append("bonus")
                if product_id and not user_summa.product_id:
                    user_summa.product_id = product_id
                    update_fields.append("product")
                if update_fields:
                    user_summa.save(update_fields=update_fields)
                self._count("user_summas.matched")

    # -- orders / cart --------------------------------------------------------

    def _migrate_orders(self, order_rows, user_map, store_map):
        # Order has no natural unique field of its own, but usta's created_at is a
        # precise (millisecond) per-row timestamp — combined with the user, it's a
        # stable, source-derived key that makes this step safe to rerun. The lookup
        # value has to be parsed the same way Django will have stored it (created_at
        # is auto_now_add, so the actual value only ever lands via _force_created_at).
        order_map = {}
        for row in order_rows:
            fields = row["fields"]
            user_id = user_map.get(fields["user"])
            if not user_id:
                self._count("orders.skipped_no_user")
                continue
            created_at = parse_datetime(fields["created_at"]) if fields.get("created_at") else None
            order, created = Order.objects.get_or_create(
                user_id=user_id,
                created_at=created_at,
                defaults={
                    "store_id": store_map.get(fields.get("store")),
                    "total_price": fields["total"],
                    "is_completed": fields["is_completed"],
                    "state": "completed" if fields["is_completed"] else "checking",
                },
            )
            if created:
                _force_created_at(order, fields.get("created_at"))
                self._count("orders.created")
            else:
                self._count("orders.matched")
            order_map[row["pk"]] = order.id
        return order_map

    def _migrate_order_items(self, order_product_rows, order_map, product_map):
        for row in order_product_rows:
            fields = row["fields"]
            order_id = order_map.get(fields["order"])
            product_id = product_map.get(fields["product"])
            if not order_id or not product_id:
                self._count("order_items.skipped")
                continue
            order = Order.objects.get(pk=order_id)
            product = Product.objects.get(pk=product_id)
            OrderItem.objects.get_or_create(
                order=order,
                user=order.user,
                product=product,
                defaults={"price": product.price, "quantity": fields["count"]},
            )
            self._count("order_items.created")

    def _migrate_carts(self, cart_rows, user_map, product_map):
        cart_by_user = {}
        for row in cart_rows:
            fields = row["fields"]
            user_id = user_map.get(fields["user"])
            product_id = product_map.get(fields["product"])
            if not user_id or not product_id:
                self._count("cart_items.skipped")
                continue

            cart_id = cart_by_user.get(user_id)
            if not cart_id:
                cart, _ = Cart.objects.get_or_create(user_id=user_id)
                cart_id = cart.id
                cart_by_user[user_id] = cart_id

            product = Product.objects.get(pk=product_id)
            CartItem.objects.get_or_create(
                cart_id=cart_id,
                product=product,
                defaults={"quantity": fields["count"], "price": product.price},
            )
            self._count("cart_items.created")
