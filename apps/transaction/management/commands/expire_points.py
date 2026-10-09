from django.core.management.base import BaseCommand
from apps.transaction.services.bonus_service import BonusService


class Command(BaseCommand):
    help = "Process 1-year point expiry and send 7-day expiration warnings."

    def handle(self, *args, **options):
        self.stdout.write("Processing expired bonus points...")
        stats = BonusService.process_expired_points()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully expired {stats['expired_count']} claims "
                f"({stats['expired_summa']} points total). "
                f"Sent {stats['warned_count']} warning notifications."
            )
        )
