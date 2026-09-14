from modeltranslation.translator import TranslationOptions, register

from apps.shared.models import AppInfo, FAQ, TrainingVideo


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


@register(AppInfo)
class AppInfoTranslationOptions(TranslationOptions):
    fields = ("working_hours",)


@register(TrainingVideo)
class TrainingVideoTranslationOptions(TranslationOptions):
    fields = ("name", "description")
