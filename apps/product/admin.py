from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.product.models import Category, SubCategory, Product


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name')


@admin.register(SubCategory)
class SubCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', 'category')


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', 'price', 'bonus_price', 'category', 'is_active')
    list_filter = ('is_active', 'category')