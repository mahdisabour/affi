from django.db.models.signals import post_save
from django.dispatch import receiver

from ..financial.models import Wallet
from .models import User, OTP
from .tasks import disableOTP, send_sms


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            user=instance
        ) 


@receiver(post_save, sender=OTP)
def otp_send_sms(sender, instance, created, *args, **kwargs):
    if created:
        phone_number = instance.user.phone_number
        send_sms.apply_async((phone_number, instance.message))


@receiver(post_save, sender=OTP)
def otp_time_arrive(sender, instance, *args, **kwargs):
    disableOTP.apply_async((instance.id, ), countdown=120)