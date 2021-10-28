from django.db import models

from . import TransactionState, TransactionType


class Wallet(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.PositiveBigIntegerField(default=0)
    bank_account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(
        max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField("core.User", on_delete=models.CASCADE)


class Transaction(models.Model):
    transaction_date = models.DateTimeField(auto_now=True)
    origin = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions")
    destination = models.ForeignKey(
        Wallet, on_delete=models.CASCADE)
    related_order = models.OneToOneField(
        "affiliation.Order", on_delete=models.CASCADE, null=True, blank=True)
    transaction_state = models.CharField(
        max_length=50, choices=TransactionState.CHOICES, default=TransactionState.PENDING)

    @property
    def amount(self):
        products = self.related_order.related_products.all()
        amount = 0
        for product in products:
            affiliation_price = int(
                (product.price)*(product.affiliate_rate / 100))
            amount = amount + affiliation_price
        return amount
