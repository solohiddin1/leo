from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from modeltranslation.translator import TranslationOptions, register

from apps.product.models import Category, Product, SubCategory
from apps.user.models import Job


class CustomAdmin(TranslationAdmin):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class StackedAdmin(TranslationStackedInline):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            # 'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ("title",)
