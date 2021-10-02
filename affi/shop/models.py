from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ..core.models import User
from . import ShopType
from .managers import ShopManager



class Shop(models.Model):

    objects = ShopManager()

    name = models.CharField(max_length=50, blank=False)
    url = models.URLField(max_length=200, blank=False)
    type = models.CharField(max_length=50, choices=ShopType.CHOICES, default=ShopType.WOOCOMMERCE)
    shop_pic = models.ImageField(
        upload_to='profile/', default="profile/default_shop_pic.png")
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.role = User.Roles.SHOP
            self.user.save()
        return super().save(*args, **kwargs)


class ShopRate(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    aff = models.ForeignKey("user.Aff", on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)

    class Meta:
        unique_together = [
            ['aff', 'shop']
        ]