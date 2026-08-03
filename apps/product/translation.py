from modeltranslation.translator import register, TranslationOptions
from apps.product.models import Product, Category, SubCategory

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )