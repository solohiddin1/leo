from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin

from apps.product.models import Category, Image, Product, SubCategory
from apps.product.translation import CustomAdmin, StackedAdmin


def image_preview(self, obj):
    image = obj.image_compressed or obj.image
    if not image:
        return "-"
    return format_html(
        '<img src="{}" style="max-height:150px; max-width:150px; object-fit:cover;" />',
        image.url,
    )

def image_preview_for_product(self, obj):
    first_image = obj.images.first()
    if not first_image:
        return "-"

    # Use compressed image if available, fallback to original
    image_file = first_image.image_compressed or first_image.image
    return format_html(
        '<img src="{}" style="max-height:60px; max-width:60px; object-fit:cover;" />',
        image_file.url,
    )

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
    list_display = ("id", "name_uz", "name_ru", "price", "bonus_price", "category",
                    "is_active", "image_preview")
    list_filter = ("is_active", "category")
    inlines = [ImageInline]
    image_preview = image_preview_for_product
