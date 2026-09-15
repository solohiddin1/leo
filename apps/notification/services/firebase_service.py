import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging

_firebase_app: firebase_admin.App | None = None


def _get_firebase_app() -> firebase_admin.App:
    global _firebase_app
    if _firebase_app is None:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app


class FirebaseService:
    @staticmethod
    def send_to_token(
        token: str,
        title: str,
        body: str,
        data: dict | None = None,
        image: str | None = None,
    ) -> str:
        _get_firebase_app()
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body, image=image),
            data={str(k): str(v) for k, v in (data or {}).items()},
            token=token,
            android=messaging.AndroidConfig(priority="high"),
        )
        return messaging.send(message)
