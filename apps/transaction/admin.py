from django.contrib import admin

from apps.transaction.models import Bonus, BonusCode, UserSumma, UserSummaImage


class BonusCodeInline(admin.TabularInline):
    model = BonusCode
    extra = 1
    fields = ('code', 'is_used')


class BonusInline(admin.TabularInline):
    model = Bonus
    extra = 1
    fields = ('summa', 'prefix', 'quantity')
    max_num = 50
    verbose_name = "Bonus"
    verbose_name_plural = "Bonuses"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')[:10]

@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'summa', 'prefix', 'quantity', 'code_count')
    list_select_related = ('product',)
    # inlines = [BonusCodeInline]

    def code_count(self, obj):
        return obj.codes.count()
    code_count.short_description = 'Generated'


@admin.register(BonusCode)
class BonusCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'bonus_info', 'is_used', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('code',)
    list_select_related = ('bonus', 'bonus__product')

    def bonus_info(self, obj):
        return str(obj.bonus)
    bonus_info.short_description = 'Bonus'


class UserSummaImageInline(admin.TabularInline):
    model = UserSummaImage
    extra = 0
    readonly_fields = ('image',)


@admin.register(UserSumma)
class UserSummaAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_code', 'summa', 'is_expired', 'created_at')
    list_filter = ('is_expired',)
    search_fields = ('code__code', 'user__username')
    readonly_fields = ('user', 'bonus', 'code', 'summa', 'created_at')
    list_select_related = ('user', 'bonus', 'code')
    inlines = [UserSummaImageInline]

    def get_code(self, obj):
        return obj.code.code
    get_code.short_description = 'Code'
