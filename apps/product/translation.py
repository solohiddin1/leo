from modeltranslation.translator import register, TranslationOptions
from apps.product.models import Product, Category, SubCategory
from apps.user.models import Job


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ('title', )