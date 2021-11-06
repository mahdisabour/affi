from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Transaction


@receiver(post_save, sender=Transaction)
def transform_transactions(sender, instance, created, **kwargs):
    if not created:
        if instance.is_staff and instance.transaction_state != "success":
            affiliate_amount = instance.amount
            instance.origin.amount -= affiliate_amount
            instance.destination.amount += affiliate_amount
            instance.origin.save()
            instance.destination.save()
            instance.transaction_state = "success"
            instance.save()