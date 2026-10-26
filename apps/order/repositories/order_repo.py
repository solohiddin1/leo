from django.db import transaction
from django.db.models import QuerySet

from apps.notification.messages import NotificationMessages
from apps.notification.services.admin_telegram_service import AdminTelegramNotifier
from apps.notification.services.notification_service import NotificationService
from apps.order.models import Order, OrderItem, OrderProblemImage, OrderState
from apps.user.models import User


class OrderRepo:
    @staticmethod
    def get_user_orders(user: User) -> QuerySet[Order]:
        return Order.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_active_orders(user: User) -> QuerySet[Order]:
        return Order.objects.filter(
            user=user,
            is_completed=False,
        ).exclude(state=OrderState.CANCELLED).order_by("-created_at")

    @staticmethod
    def get_order_by_id(user: User, order_id: int) -> Order | None:
        return Order.objects.filter(user=user, id=order_id).first()

    @staticmethod
    def approve_order(order: Order) -> Order:
        if order.state != OrderState.ACCEPTED:
            order.state = OrderState.ACCEPTED
            order.save(update_fields=["state", "updated_at"])

            user = order.user
            admin_msg = (
                f"✅ <b>Buyurtma Qabul Qilindi (Approved)!</b>\n\n"
                f"<b>Order ID:</b> #{order.id}\n"
                f"<b>Mijoz:</b> {user.first_name} {user.last_name} (@{user.telegram_username or 'N/A'})\n"
                f"<b>Summa:</b> {order.total_price} so'm"
            )
            AdminTelegramNotifier.send(admin_msg)

            title, body = NotificationMessages.order_approved_msg.render(user.lang, order_id=order.id)

            NotificationService.send_to_user(
                user=user,
                title=title,
                body=body,
                notification_type="ORDER",
                data={"order_id": str(order.id), "status": "accepted"},
            )

        return order

    @staticmethod
    @transaction.atomic
    def reject_order(order: Order) -> Order:
        if order.state != OrderState.CANCELLED:
            user = order.user
            user.balance += order.total_price
            user.save(update_fields=["balance"])

            order.state = OrderState.CANCELLED
            order.save(update_fields=["state", "updated_at"])

            admin_msg = (
                f"❌ <b>Buyurtma Bekor Qilindi (Rejected)!</b>\n\n"
                f"<b>Order ID:</b> #{order.id}\n"
                f"<b>Mijoz:</b> {user.first_name} {user.last_name} (@{user.telegram_username or 'N/A'})\n"
                f"<b>Qaytarilgan summa:</b> {order.total_price} so'm"
            )
            AdminTelegramNotifier.send(admin_msg)

            title, body = NotificationMessages.order_rejected_msg.render(
                user.lang, order_id=order.id, total_price=order.total_price
            )

            NotificationService.send_to_user(
                user=user,
                title=title,
                body=body,
                notification_type="ORDER",
                data={"order_id": str(order.id), "status": "cancelled"},
            )

        return order

    @staticmethod
    def complete_order(order: Order) -> Order:
        order.is_completed = True
        order.state = OrderState.COMPLETED
        order.save(update_fields=["is_completed", "state", "updated_at"])

        user = order.user
        admin_msg = (
            f"🎉 <b>Buyurtma Yakunlandi (Completed)!</b>\n\n"
            f"<b>Order ID:</b> #{order.id}\n"
            f"<b>Mijoz:</b> {user.first_name} {user.last_name} (@{user.telegram_username or 'N/A'})\n"
            f"<b>Telegram ID:</b> {user.telegram_id or 'N/A'}\n"
            f"<b>Summa:</b> {order.total_price} so'm"
        )
        AdminTelegramNotifier.send(admin_msg)

        title, body = NotificationMessages.order_completed_msg.render(user.lang, order_id=order.id)

        NotificationService.send_to_user(
            user=user,
            title=title,
            body=body,
            notification_type="ORDER",
            data={"order_id": str(order.id), "status": "completed"},
        )

        return order

    @staticmethod
    def report_order_problem(order: Order, problem_note: str, images: list = None) -> Order:
        order.problem_note = problem_note
        order.save(update_fields=["problem_note", "updated_at"])

        created_images = []
        if images:
            for img in images:
                problem_img = OrderProblemImage.objects.create(order=order, image=img)
                created_images.append(problem_img)

        user = order.user
        msg = (
            f"⚠️ <b>Order Problem Reported!</b>\n\n"
            f"<b>Order ID:</b> #{order.id}\n"
            f"<b>Client:</b> {user.first_name} {user.last_name} (@{user.telegram_username or 'N/A'})\n"
            f"<b>Telegram ID:</b> {user.telegram_id or 'N/A'}\n"
            f"<b>Total Price:</b> {order.total_price}\n"
            f"<b>Problem Note:</b> {problem_note or 'No description provided'}"
        )

        if created_images:
            for idx, img_obj in enumerate(created_images):
                caption = msg if idx == 0 else f"Order #{order.id} problem photo #{idx + 1}"
                AdminTelegramNotifier.send_photo(img_obj.image, caption=caption)
        else:
            AdminTelegramNotifier.send(msg)

        return order

    @staticmethod
    @transaction.atomic
    def create_order_from_items(user: User, cart_items: QuerySet, store_id: int = None) -> Order | None:
        items = list(cart_items.select_related("product"))
        if not items:
            return None

        if any(not item.product.is_active or (item.product.price or 0) <= 0 for item in items):
            return None

        total_price = sum(item.price * item.quantity for item in items)

        if user.balance < total_price:
            return None

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            store_id=store_id
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                user=user,
                product=item.product,
                price=item.price,
                quantity=item.quantity,
            )
            for item in items
        ])

        user.balance -= total_price
        user.save(update_fields=['balance'])

        cart_items.delete()

        product_lines = []
        photos_to_send = []
        seen_product_ids = set()

        for item in items:
            product = item.product
            item_summa = item.price * item.quantity
            item_summa_str = f"{item_summa:,}".replace(",", " ")
            product_lines.append(f"• <b>{product.name}</b> x {item.quantity} = {item_summa_str} so'm")

            if product.id not in seen_product_ids:
                seen_product_ids.add(product.id)
                img = product.images.first()
                if img and img.image:
                    photos_to_send.append((img.image, f"📦 <b>{product.name}</b>"))

        products_text = "\n".join(product_lines) if product_lines else "N/A"
        store_line = f"<b>Do'kon:</b> {order.store.name}\n" if order.store else ""
        total_price_str = f"{order.total_price:,}".replace(",", " ")

        admin_msg = (
            f"🆕 <b>Yangi Buyurtma Yaratildi!</b>\n\n"
            f"<b>Order ID:</b> #{order.id}\n"
            f"<b>Mijoz:</b> {user.first_name} {user.last_name} (@{user.telegram_username or 'N/A'})\n"
            f"<b>Telegram ID:</b> {user.telegram_id or 'N/A'}\n"
            f"<b>Telefon:</b> {user.username}\n"
            f"{store_line}"
            f"<b>Mahsulotlar:</b>\n{products_text}\n\n"
            f"<b>Summa:</b> {total_price_str} so'm"
        )
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "✅ Tasdiqlash", "callback_data": f"approve_order_{order.id}"},
                    {"text": "❌ Bekor qilish", "callback_data": f"reject_order_{order.id}"},
                ]
            ]
        }
        AdminTelegramNotifier.send_media_and_message(
            photos=photos_to_send,
            text=admin_msg,
            reply_markup=reply_markup,
        )

        title, body = NotificationMessages.order_created_msg.render(user.lang, order_id=order.id)
        NotificationService.send_to_user(
            user=user,
            title=title,
            body=body,
            notification_type="ORDER",
            data={"order_id": str(order.id), "status": "created"},
        )

        return order
