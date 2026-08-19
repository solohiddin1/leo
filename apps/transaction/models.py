from django.db import models

from apps.product.models import Product
from apps.user.models import User


class Bonus(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, 'bonuses', blank=True, null=True)
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    summa = models.IntegerField(default=1, verbose_name="Сумма", blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'


class UserSumma(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'points')
    bonus = models.ForeignKey(Bonus, models.SET_NULL, 'redemptions', null=True, blank=True,
                              verbose_name="Бонус")
    code = models.CharField(max_length=500)
    # The amount granted at redemption time — Bonus.summa may be edited later, and the
    # expiry job must give back exactly what was given.
    summa = models.IntegerField(default=0, verbose_name="Сумма")
    is_expired = models.BooleanField(default=False, verbose_name="Истёк")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
