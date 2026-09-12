from django.core.management.base import BaseCommand, CommandError
from firebase_admin import messaging

from apps.notification.services.firebase_service import FirebaseService


class Command(BaseCommand):
    help = "Send a test push notification directly to an FCM token (bypasses the Device/User models)."

    def add_arguments(self, parser):
        parser.add_argument("token", help="FCM registration token to send the test notification to")
        parser.add_argument("--title", default="Test notification", help="Notification title")
        parser.add_argument("--body", default="This is a test notification.", help="Notification body")

    def handle(self, *args, **options):
        token = options["token"]
        title = options["title"]
        body = options["body"]

        try:
            for i in range(100):
                message_id = FirebaseService.send_to_token(token, title, body)
        except messaging.UnregisteredError as exc:
            raise CommandError(f"Token is unregistered/invalid: {exc}") from exc
        except Exception as exc:
            raise CommandError(f"Failed to send notification: {exc}") from exc

        self.stdout.write(self.style.SUCCESS(f"Notification sent. Message ID: {message_id}"))
