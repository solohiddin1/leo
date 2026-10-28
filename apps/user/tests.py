from unittest.mock import patch

from django.contrib import admin
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.notification.messages import NotificationMessages
from apps.user.models import User


class AdminInitializationTest(TestCase):
    def test_admin_site_loads(self):
        admin.autodiscover()


class UserLangUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            first_name="Test",
            last_name="User",
            lang="uz",
            is_verified=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_update_lang_via_dedicated_endpoint_patch(self):
        url = reverse("update_lang")
        response = self.client.patch(url, {"lang": "ru"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.lang, "ru")

    def test_update_lang_via_lang_endpoint_post(self):
        url = reverse("update_lang")
        response = self.client.post(url, {"lang": "ru"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.lang, "ru")

    def test_update_lang_via_profile_update_endpoint(self):
        url = reverse("profile_update")
        response = self.client.patch(url, {"lang": "ru", "first_name": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.lang, "ru")
        self.assertEqual(self.user.first_name, "Updated")

    def test_update_lang_invalid_choice(self):
        url = reverse("update_lang")
        response = self.client.patch(url, {"lang": "fr"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(self.user.lang, "uz")


class NotificationLanguageTestCase(APITestCase):
    def test_order_created_notification_languages(self):
        title_uz, body_uz = NotificationMessages.order_created_msg.render("uz", order_id=123)
        self.assertIn("Yangi buyurtma", title_uz)
        self.assertIn("#123", body_uz)

        title_ru, body_ru = NotificationMessages.order_created_msg.render("ru", order_id=123)
        self.assertIn("Новый заказ", title_ru)
        self.assertIn("№#123", body_ru)

    def test_order_approved_notification_languages(self):
        title_uz, body_uz = NotificationMessages.order_approved_msg.render("uz", order_id=456)
        self.assertIn("qabul qilindi", title_uz)

        title_ru, body_ru = NotificationMessages.order_approved_msg.render("ru", order_id=456)
        self.assertIn("Заказ принят", title_ru)
        self.assertIn("подтверждён", body_ru)

    def test_order_rejected_notification_languages(self):
        title_uz, body_uz = NotificationMessages.order_rejected_msg.render("uz", order_id=789, total_price=50000)
        self.assertIn("bekor qilindi", title_uz)
        self.assertIn("50000", body_uz)

        title_ru, body_ru = NotificationMessages.order_rejected_msg.render("ru", order_id=789, total_price=50000)
        self.assertIn("Заказ отменён", title_ru)
        self.assertIn("50000 баллов возвращено", body_ru)

    def test_bonus_registered_notification_languages(self):
        title_uz, body_uz = NotificationMessages.bonus_create_msg.render("uz", code="CODE123", summa=10000)
        self.assertIn("Bonus kod", title_uz)

        title_ru, body_ru = NotificationMessages.bonus_create_msg.render("ru", code="CODE123", summa=10000)
        self.assertIn("Бонусный код", title_ru)
        self.assertIn("CODE123", body_ru)

    def test_bonus_approved_notification_languages(self):
        title_uz, body_uz = NotificationMessages.bonus_approved_msg.render("uz", summa=10000)
        self.assertIn("tasdiqlandi", title_uz)

        title_ru, body_ru = NotificationMessages.bonus_approved_msg.render("ru", summa=10000)
        self.assertIn("подтверждён", title_ru)

    def test_challenge_completed_notification_languages(self):
        title_uz, body_uz = NotificationMessages.challenge_completed_msg.render("uz", challenge_title="Speed", reward=5000)
        self.assertIn("yakunlandi", title_uz)

        title_ru, body_ru = NotificationMessages.challenge_completed_msg.render("ru", challenge_title="Speed", reward=5000)
        self.assertIn("Челлендж завершён", title_ru)
        self.assertIn("«Speed»", body_ru)


class TelegramLoginOtpTestCase(APITestCase):
    def setUp(self):
        from unittest.mock import patch
        from apps.shared.models import SiteConfig
        SiteConfig.objects.create(send_otp_code=True, otp_wait_seconds=60)

    @patch("apps.user.services.telegram.TelegramClient.send_message")
    def test_new_user_login_with_contact_reply(self, mock_send):
        from apps.user.services.telegram import TgOtpService
        from apps.user.models import TelegramLoginToken, User, Otp

        # 1. Request OTP deep link
        res = TgOtpService.request()
        token = res["token"]
        self.assertFalse(res["poll"])

        # 2. User presses /start <token>
        start_update = {
            "update_id": 1,
            "message": {
                "message_id": 10,
                "from": {"id": 123456, "first_name": "Aziz", "username": "aziz"},
                "chat": {"id": 123456},
                "text": f"/start {token}",
            },
        }
        TgOtpService.handle_update(start_update)

        token_row = TelegramLoginToken.objects.get(token=token)
        self.assertEqual(token_row.telegram_id, 123456)
        self.assertEqual(token_row.status, "PENDING")
        self.assertIsNone(token_row.user)

        # 3. User responds with contact in reply to bot's message
        contact_update = {
            "update_id": 2,
            "message": {
                "message_id": 12,
                "from": {"id": 123456, "first_name": "Aziz", "username": "aziz"},
                "chat": {"id": 123456},
                "reply_to_message": {
                    "message_id": 11,
                    "from": {"id": 999, "is_bot": True},
                    "text": "Kirishni yakunlash uchun telefon raqamingizni ulashing 👇",
                },
                "contact": {
                    "phone_number": "+998901234567",
                    "first_name": "Aziz",
                    "user_id": 123456,
                },
            },
        }
        TgOtpService.handle_update(contact_update)

        token_row.refresh_from_db()
        self.assertIsNotNone(token_row.user)
        self.assertEqual(token_row.user.username, "998901234567")
        self.assertEqual(token_row.user.telegram_id, "123456")

        # Check that OTP was created
        otp = Otp.objects.filter(user=token_row.user).first()
        self.assertIsNotNone(otp)

        # 4. Verify OTP
        verify_res = TgOtpService.verify_otp(token, otp.code)
        self.assertEqual(verify_res.get("status"), "CONFIRMED")
        self.assertIn("access", verify_res)

    @patch("apps.user.services.telegram.TelegramClient.send_message")
    def test_new_user_login_with_text_phone(self, mock_send):
        from apps.user.services.telegram import TgOtpService
        from apps.user.models import TelegramLoginToken, Otp

        res = TgOtpService.request()
        token = res["token"]

        # /start
        TgOtpService.handle_update({
            "update_id": 1,
            "message": {
                "message_id": 20,
                "from": {"id": 654321, "first_name": "Botir"},
                "chat": {"id": 654321},
                "text": f"/start {token}",
            },
        })

        # User types phone as text replying to bot
        TgOtpService.handle_update({
            "update_id": 2,
            "message": {
                "message_id": 22,
                "from": {"id": 654321, "first_name": "Botir"},
                "chat": {"id": 654321},
                "reply_to_message": {
                    "message_id": 21,
                    "from": {"id": 999, "is_bot": True},
                    "text": "Kirishni yakunlash uchun telefon raqamingizni ulashing 👇",
                },
                "text": "909876543",
            },
        })

        token_row = TelegramLoginToken.objects.get(token=token)
        self.assertIsNotNone(token_row.user)
        self.assertEqual(token_row.user.username, "998909876543")

        otp = Otp.objects.filter(user=token_row.user).first()
        self.assertIsNotNone(otp)

    @patch("apps.notification.services.admin_telegram_service.AdminTelegramNotifier.edit_message_text")
    @patch("apps.notification.services.admin_telegram_service.AdminTelegramNotifier.answer_callback_query")
    def test_approve_and_reject_order_callback(self, mock_answer, mock_edit):
        from apps.order.models import Order, OrderState
        from apps.user.models import User
        from apps.user.services.telegram import TgOtpService

        user = User.objects.create_user(
            username="998901112233",
            first_name="TestBuyer",
            balance=100000,
        )
        order = Order.objects.create(
            user=user,
            total_price=50000,
            state=OrderState.CHECKING,
        )

        # Test Approve
        TgOtpService.handle_update({
            "update_id": 100,
            "callback_query": {
                "id": "cb_1",
                "from": {"id": 111, "first_name": "AdminUser", "username": "admin_one"},
                "message": {"message_id": 99, "chat": {"id": -100123}, "text": f"Order #{order.id}"},
                "data": f"approve_order_{order.id}",
            },
        })

        order.refresh_from_db()
        self.assertEqual(order.state, OrderState.ACCEPTED)
        mock_answer.assert_called_with("cb_1", text="✅ Buyurtma tasdiqlandi!")
        mock_edit.assert_called_once()
        args, kwargs = mock_edit.call_args
        self.assertEqual(kwargs.get("reply_markup"), {"inline_keyboard": []})
        self.assertIn("Tasdiqlandi (@admin_one)", args[2])

        # Test Reject on a new checking order
        order2 = Order.objects.create(
            user=user,
            total_price=40000,
            state=OrderState.CHECKING,
        )
        initial_balance = user.balance
        mock_edit.reset_mock()
        mock_answer.reset_mock()

        TgOtpService.handle_update({
            "update_id": 101,
            "callback_query": {
                "id": "cb_2",
                "from": {"id": 111, "first_name": "AdminUser", "username": "admin_one"},
                "message": {"message_id": 100, "chat": {"id": -100123}, "text": f"Order #{order2.id}"},
                "data": f"reject_order_{order2.id}",
            },
        })

        order2.refresh_from_db()
        self.assertEqual(order2.state, OrderState.CANCELLED)
        user.refresh_from_db()
        self.assertEqual(user.balance, initial_balance + 40000)
        mock_answer.assert_called_with("cb_2", text="❌ Buyurtma bekor qilindi!")
        mock_edit.assert_called_once()
        args2, kwargs2 = mock_edit.call_args
        self.assertEqual(kwargs2.get("reply_markup"), {"inline_keyboard": []})
        self.assertIn("Bekor qilindi (@admin_one)", args2[2])


