from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transaction.models import Bonus, BonusCode


@receiver(post_save, sender=Bonus)
def generate_bonus_codes(sender, instance: Bonus, **kwargs):
    if not instance.prefix or instance.quantity <= 0:
        return

    existing_count = instance.codes.count()
    needed = instance.quantity - existing_count
    if needed <= 0:
        return

    new_codes = []
    serial = existing_count + 1
    while len(new_codes) < needed:
        letter = chr(ord('A') + serial % 26)
        code_str = f"{instance.prefix}{letter}{serial:04d}"
        new_codes.append(BonusCode(bonus=instance, code=code_str))
        serial += 1

    BonusCode.objects.bulk_create(new_codes, ignore_conflicts=True)
