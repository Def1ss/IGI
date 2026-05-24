from django.contrib import admin
from .models import PromoCode, PromoCodeUsage

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount_percent', 'valid_from', 'valid_to', 'is_active', 'applicable_to')
    list_filter = ('is_active', 'applicable_to')
    search_fields = ('code',)

@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'promo_code', 'client', 'used_at', 'discount_applied')
    list_filter = ('used_at',)
    search_fields = ('client__user__username', 'promo_code__code')
