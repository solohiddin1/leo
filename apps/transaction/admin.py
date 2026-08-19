from django.contrib import admin

from apps.transaction.models import Bonus, UserSumma


class BonusInline(admin.TabularInline):
    model = Bonus
    extra = 0
    fields = ('code', 'summa')


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('code', 'product', 'summa')
    search_fields = ('code',)
    list_select_related = ('product',)


@admin.register(UserSumma)
class UserSummaAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'summa', 'is_expired', 'created_at')
    list_filter = ('is_expired',)
    search_fields = ('code', 'user__username')
    readonly_fields = ('user', 'bonus', 'code', 'summa', 'created_at')
    list_select_related = ('user', 'bonus')
