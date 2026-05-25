# apps/promocodes/services.py
from decimal import Decimal
from django.utils import timezone

from apps.promocodes.models import PromoCode, PromoCodeUsage


def apply_discount(base_price, discount_percent):
    percent = int(discount_percent or 0)
    return round(float(base_price) * (1 - percent / 100), 2)


def validate_promo_code(code, service_type):
    if not code:
        return None, 'Введите промокод'
    promo = PromoCode.objects.filter(code__iexact=code.strip()).first()
    if not promo:
        return None, 'Промокод не найден'
    if not promo.is_active:
        return None, 'Этот промокод деактивирован'
    now = timezone.now()
    if now < promo.valid_from or now > promo.valid_to:
        return None, 'Срок действия промокода еще не начался или уже истек'
    if promo.applicable_to != 'all' and promo.applicable_to != service_type:
        return None, f'Этот промокод неприменим для категории услуги: {service_type}'
    return promo, None


def record_promo_usage(promo, client, base_price, final_price):
    if promo and float(base_price) > float(final_price):
        PromoCodeUsage.objects.create(
            promo_code=promo,
            client=client,
            discount_applied=Decimal(str(round(float(base_price) - float(final_price), 2))),
        )

def sessions_overlap(start_a, end_a, start_b, end_b):
    return start_a < end_b and end_a > start_b