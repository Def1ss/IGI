from django.db import models

class PromoCode(models.Model):
    CODE_CATEGORIES = [
        ('all', 'Все виды услуг'),
        ('group', 'Групповые занятия'),
        ('individual', 'Индивидуальные занятия'),
        ('club_card', 'Клубная карта'),
    ]
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applicable_to = models.CharField(max_length=20, choices=CODE_CATEGORIES, default='all')

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"


class PromoCodeUsage(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='usages')
    client = models.ForeignKey('users.Client', on_delete=models.CASCADE, related_name='promocode_usages')
    used_at = models.DateTimeField(auto_now_add=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.client} использовал {self.promo_code.code} (Скидка {self.discount_applied})"
