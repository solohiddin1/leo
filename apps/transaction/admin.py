from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.shortcuts import render

from apps.shared.utils.preview import image_preview_with_no_compressed
from apps.transaction.models import Bonus, BonusCode, UserSumma, UserSummaImage, Challenge
from apps.transaction.services.bonus_service import BonusService


class RejectClaimForm(forms.Form):
    reason = forms.CharField(label='Rejection reason', widget=forms.Textarea, max_length=255)


class BonusCodeInline(admin.TabularInline):
    model = BonusCode
    extra = 1
    fields = ('code', 'is_used')


class BonusInline(admin.TabularInline):
    model = Bonus
    extra = 1
    fields = ('summa', 'prefix', 'quantity')
    max_num = 10
    verbose_name = "Bonus"
    verbose_name_plural = "Bonuses"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')

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
    list_filter = ('is_used', 'bonus')
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
    list_display = ('user', 'get_code', 'product', 'status', 'summa', 'is_expired', 'created_at')
    list_filter = ('is_expired', 'product')
    search_fields = ('code__code', 'user__username')
    readonly_fields = ('user', 'bonus', 'code', 'product', 'summa', 'created_at')
    list_select_related = ('user', 'bonus', 'code', 'product')
    inlines = [UserSummaImageInline]
    actions = ['approve_bonus_codes', 'reject_bonus_codes']

    def get_code(self, obj):
        return obj.code.code
    get_code.short_description = 'Code'

    def approve_bonus_codes(self, request, queryset):
        approved = failed = 0
        for claim in queryset:
            response = BonusService.approve_claim(claim.id, request.user)
            if response.status_code == 200:
                approved += 1
            else:
                failed += 1

        if approved:
            self.message_user(request, f"{approved} claim(s) approved.", level=messages.SUCCESS)
        if failed:
            self.message_user(
                request, f"{failed} claim(s) could not be approved (not pending).", level=messages.WARNING,
            )
    approve_bonus_codes.short_description = 'Approve bonus claims'

    def reject_bonus_codes(self, request, queryset):
        if 'apply' in request.POST:
            form = RejectClaimForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                rejected = failed = 0
                for claim in queryset:
                    response = BonusService.reject_claim(claim.id, request.user, reason)
                    if response.status_code == 200:
                        rejected += 1
                    else:
                        failed += 1

                if rejected:
                    self.message_user(request, f"{rejected} claim(s) rejected.", level=messages.SUCCESS)
                if failed:
                    self.message_user(
                        request, f"{failed} claim(s) could not be rejected (not pending).", level=messages.WARNING,
                    )
                return None
        else:
            form = RejectClaimForm()

        return render(
            request,
            'admin/transaction/reject_claims_confirmation.html',
            context={
                'claims': queryset,
                'form': form,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
            },
        )
    reject_bonus_codes.short_description = 'Reject bonus claims'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    actions = ['activate_challenges', 'deactivate_challenges']

    def activate_challenges(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_challenges(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(UserSummaImage)
class UserSummaImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_summa', 'image', 'image_preview')
    image_preview = image_preview_with_no_compressed
    image_preview.short_description = 'Image Preview'
