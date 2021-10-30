from django.db.models import Sum, Count

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from ...shop.models import Shop
from ...product.models import Product
from ...category.models import Category
from .types import PlainTextNode, ShopNode, Overview
from .filters import ShopFilter

from ...financial.models import Transaction
from ..product.types import TopProduct
from ..category.types import TopCategory

class ShopQuery(graphene.ObjectType):
    shop = graphene.Field(ShopNode, id=graphene.Int())
    all_shop = DjangoFilterConnectionField(ShopNode, filterset_class=ShopFilter)

    def resolve_shop(self, info, id):
        return Shop.objects.filter(pk=id).first()
