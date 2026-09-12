import re

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transaction.models import Bonus, BonusCode

_STRIP_ZEROS_RE = re.compile(r"^(.*?)(0*)$")


@receiver(post_save, sender=Bonus)
def generate_bonus_codes(sender, instance: Bonus, created, **kwargs):
    if not created:
        return

    if not instance.prefix or instance.quantity <= 0:
        return

    match = _STRIP_ZEROS_RE.match(instance.prefix)
    clean_prefix = match.group(1) if match else instance.prefix

    existing_codes = set(
        BonusCode.objects.filter(code__startswith=clean_prefix)
        .values_list('code', flat=True)
    )

    new_codes = []
    serial = 1

    while len(new_codes) < instance.quantity:
        letter = chr(ord('A') + (serial % 26))

        code_str = f"{clean_prefix}{letter}{serial:04d}"

        if code_str not in existing_codes:
            new_codes.append(BonusCode(bonus=instance, code=code_str))
            existing_codes.add(code_str)

        serial += 1

    BonusCode.objects.bulk_create(new_codes, ignore_conflicts=True)
