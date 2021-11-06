from django.db import models

from . import OrderStatus


class Affiliation(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    affiliator = models.ForeignKey("user.Aff", on_delete=models.CASCADE)
    related_shop = models.ForeignKey(
        "shop.Shop", on_delete=models.CASCADE, blank=True, null=True)
    affiliation_url = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = [
            ['affiliator', 'related_shop']
        ]

    # def __str__(self) -> str:
    #     return f"{self.affiliator.user.name}, {self.related_shop.user.name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    base_order_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)
    related_affiliation = models.ForeignKey(
        Affiliation, on_delete=models.CASCADE)
    related_products = models.ManyToManyField("product.Product", blank=True, related_name="orders")

    class Meta:
        unique_together = [
            ['base_order_id', 'related_affiliation']
        ]

    # def __str__(self) -> str:
    #     return f"{self.related_affiliation.related_shop.user.name}"