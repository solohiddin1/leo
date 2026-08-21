from django.db import models

from apps.product.models import Product
from apps.user.models import BaseModel, User


class Bonus(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE, 'bonuses', blank=True, null=True)
    summa = models.IntegerField(default=1, verbose_name="Amount of bonus", blank=True, null=True)
    prefix = models.CharField(max_length=10, verbose_name="First 4 code of product", blank=True,
                              default="")
    quantity = models.PositiveIntegerField(default=9999, verbose_name="Amount of code")

    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'

    def __str__(self):
        return f"Bonus #{self.pk}"


class BonusCode(BaseModel):
    bonus = models.ForeignKey(Bonus, models.CASCADE, related_name='codes', verbose_name="Bonus")
    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    is_used = models.BooleanField(default=False, verbose_name="Used")

    class Meta:
        verbose_name = 'Bonus Code'
        verbose_name_plural = 'Bonus Codes'

    def __str__(self):
        return self.code


class UserSumma(BaseModel):
    user = models.ForeignKey(User, models.CASCADE, 'points')
    bonus = models.ForeignKey(Bonus, models.SET_NULL, 'redemptions', null=True, blank=True,
                              verbose_name="Бонус")
    code = models.CharField(max_length=500)
    # The amount granted at redemption time — Bonus.summa may be edited later, and the
    # expiry job must give back exactly what was given.
    summa = models.IntegerField(default=0, verbose_name="Сумма")
    is_expired = models.BooleanField(default=False, verbose_name="Истёк")

    def __str__(self):
        return self.user.username


class UserSummaImage(models.Model):
    user_summa = models.ForeignKey(UserSumma, models.CASCADE, related_name='images',
                                   verbose_name="Redemption")
    image = models.ImageField(upload_to='bonus_images/', verbose_name="Фото")

    class Meta:
        verbose_name = 'Redemption Image'
        verbose_name_plural = 'Redemption Images'

    def __str__(self):
        return f"Image for {self.user_summa}"
