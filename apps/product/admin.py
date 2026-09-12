from django.contrib import admin
from django.contrib.admin import TabularInline
from modeltranslation.admin import TabbedTranslationAdmin

from apps.product.models import Category, Image, Product, SubCategory
from apps.product.translation import CustomAdmin, StackedAdmin
from apps.shared.utils.preview import image_preview, image_preview_for_product
from apps.transaction.admin import BonusInline


class ImageInline(TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['image_compressed', "image_preview"]
    image_preview = image_preview


class SubCategoryInline(StackedAdmin):
    model = SubCategory
    fk_name = "category"
    extra = 1
    show_change_link = True
    readonly_fields = ['image_compressed', 'image_preview']
    image_preview = image_preview


class ProductImageInline(StackedAdmin):
    model = Image
    fk_name = "image"

@admin.register(Category)
class CategoryAdmin(CustomAdmin):
    inlines = (SubCategoryInline,)
    list_display = ("id", "name_uz", "name_ru", "order", "image_preview")
    readonly_fields = ['image_compressed', "image_preview"]

    image_preview = image_preview
    image_preview.short_description = "Image preview"

@admin.register(SubCategory)
class SubCategoryAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name_uz", "name_ru", "category", "image_preview")
    readonly_fields = ['image_compressed']
    image_preview = image_preview


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name_uz", "name_ru", "price", "category",
                    "is_active", "image_preview")
    list_filter = ("is_active", "category")
    inlines = [ImageInline, BonusInline]
    image_preview = image_preview_for_product
