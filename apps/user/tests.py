from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.notification.messages import NotificationMessages
from apps.user.models import User


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
        url = reverse("lang_update")
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
        self.assertIn("50000 сум возвращено", body_ru)

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
