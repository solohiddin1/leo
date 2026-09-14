from rest_framework import serializers

from apps.shared.models import AppInfo, FAQ
from apps.shared.repositories.app_info_repo import FAQRepo


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            "id",
            "question",
            "question_uz",
            "question_ru",
            "answer",
            "answer_uz",
            "answer_ru",
            "ordering",
            "is_active",
        ]


class AppInfoSerializer(serializers.ModelSerializer):
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = AppInfo
        fields = [
            "id",
            "telegram_support_username",
            "call_center_phones",
            "email_support",
            "working_hours",
            "working_hours_uz",
            "working_hours_ru",
            "faqs",
        ]

    def get_call_center_phone(self, obj):
        phones = obj.call_center_phones
        if isinstance(phones, list) and phones:
            return phones[0]
        return ""

    def get_faqs(self, obj):
        faqs = FAQRepo.get_active_faqs()
        return FAQSerializer(faqs, many=True).data
