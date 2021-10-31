from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.db.models import Sum

from ..product.models import Product
from ..category.models import Category


class TransactionManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result

    def affiliator_transactions(self, user_id, days, *args, **kwargs):
        affiliator_tranactions = self.get_queryset(*args, **kwargs).filter(
            related_order__related_affiliation__affiliator__user__id=user_id
        )
        affiliator_transaction = affiliator_tranactions.filter(
            updated_at__range=[
                timezone.now()-timezone.timedelta(days=days), timezone.now()]
        )
        return affiliator_transaction

    def shop_transactions(self, user_id, days, *args, **kwargs):
        shop_tranactions = self.get_queryset(*args, **kwargs).filter(
            related_order__related_affiliation__related_shop__user__id=user_id
        )
        shop_transaction = shop_tranactions.filter(
            updated_at__range=[
                timezone.now()-timezone.timedelta(days=days), timezone.now()]
        )
        return shop_transaction

    def shop_products_price(self, user_id, days, *args, **kwargs):
        result = Product.objects.filter( # filter producs by shop user id and time
            orders__transactions__related_order__related_affiliation__related_shop__user__id=user_id,
            orders__transactions__updated_at__range=[
                timezone.now()-timezone.timedelta(days=days), timezone.now()]
        ).aggregate(Sum("price"))["price__sum"]
        return result

    def shop_products(self, user_id):
        result = Product.objects.filter( # filter producs by shop user id
            orders__transactions__related_order__related_affiliation__related_shop__user__id=user_id
        )
        return result

    def aff_products(self, user_id):
        result = Product.objects.filter( # filter producs by shop user id
            orders__transactions__related_order__related_affiliation__affiliator__user__id=user_id
        )
        return result

    def shop_categories(self, user_id):
        Category.objects.filter(
            related_shop__user__id=user_id
        )

    def aff_categories(self, user_id):
        Category.objects.filter(
            products__orders__transactions__related_order__related_affiliation__affiliator__user__id=user_id
        )
