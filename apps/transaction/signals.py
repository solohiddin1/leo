import re

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transaction.models import Bonus, BonusCode

_PREFIX_RE = re.compile(r"^(.*?)(\d+)$")


@receiver(post_save, sender=Bonus)
def generate_bonus_codes(sender, instance: Bonus, **kwargs):
    if not instance.prefix or instance.quantity <= 0:
        return

    match = _PREFIX_RE.match(instance.prefix)
    if not match:
        return

    alpha_head, first_number = match.groups()
    width = len(first_number)
    start = int(first_number)

    existing_count = instance.codes.count()
    needed = instance.quantity - existing_count
    if needed <= 0:
        return

    new_codes = [
        BonusCode(bonus=instance, code=f"{alpha_head}{start + offset:0{width}d}")
        for offset in range(existing_count, existing_count + needed)
    ]

    BonusCode.objects.bulk_create(new_codes, ignore_conflicts=True)
