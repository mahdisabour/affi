import urllib.parse as urlparse
from urllib.parse import urlencode

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Affiliation, Order
from ..financial.models import Transaction
from .tasks import get_products_by_order

@receiver(post_save, sender=Affiliation)
def create_affiliation_url(sender, instance, created, **kwargs):
    if created:
        params = {
            "aff_id": instance.id
        }
        url = instance.related_shop.url
        instance.affiliation_url = create_url(url, params)
        instance.save()


@receiver(post_save, sender=Order)
def get_order_products(sender, instance, created, **kwargs):
    if created:
        print("get_order_products created")
        order_id = instance.id
        shop_id = instance.related_affiliation.related_shop.id
        base_order_id = instance.base_order_id
        get_products_by_order.apply_async((shop_id, base_order_id, order_id, ))


@receiver(post_save, sender=Order)
def create_transaction(sender, instance, created, **kwargs):
    if not created:
        if instance.status == "completed":
            print("create transaction not created")
            shop_user = instance.related_affiliation.related_shop.user
            aff_user = instance.related_affiliation.affiliator.user
            Transaction.objects.create(
                related_order=instance,
                origin=shop_user.wallet,
                destination=aff_user.wallet,
            )
                

def create_url(url, params):
    url_parse = urlparse.urlparse(url)
    query = url_parse.query
    url_dict = dict(urlparse.parse_qsl(query))
    url_dict.update(params)
    url_new_query = urlparse.urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    new_url = urlparse.urlunparse(url_parse)
    return new_url


