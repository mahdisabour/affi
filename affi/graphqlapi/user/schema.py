from django.utils import timezone
from django.db.models import Sum, Count

import graphene
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .types import (
    PlainTextNode,
    AffNode,
    Overview
)
from ...user.models import Aff
from ...financial.models import Transaction
from ...product.models import Product
from ...category.models import Category

from ..product.types import TopProduct
from ..category.types import TopCategory


class UserQuery(ObjectType):
    # Aff = PlainTextNode.Field(AffNode)
    all_aff = DjangoFilterConnectionField(AffNode)
    aff_overview = graphene.Field(Overview, aff_user_id=graphene.Int())
    aff_top_products = graphene.List(TopProduct, aff_user_id=graphene.Int())
    aff_top_categories = graphene.List(TopCategory, aff_user_id=graphene.Int())

    @login_required
    def resolve_aff_overview(self, info, aff_user_id):
        affiliator_Transaction_by_day = Transaction.objects.affiliator_transactions(
            user_id=aff_user_id, days=1)
        affiliator_Transaction_by_day_amount = affiliator_Transaction_by_day.aggregate(
            Sum('amount'))["amount__sum"]
        day_count = affiliator_Transaction_by_day.values(
            "related_order__related_products").count()

        affiliator_Transaction_by_month = Transaction.objects.affiliator_transactions(
            user_id=aff_user_id, days=30)
        affiliator_Transaction_by_month_amount = affiliator_Transaction_by_month.aggregate(
            Sum('amount'))["amount__sum"]
        month_count = affiliator_Transaction_by_month.values(
            "related_order__related_products").count()

        affiliator_Transaction_by_year = Transaction.objects.affiliator_transactions(
            user_id=aff_user_id, days=365)
        affiliator_Transaction_by_year_amount = affiliator_Transaction_by_year.aggregate(
            Sum('amount'))["amount__sum"]
        year_count = affiliator_Transaction_by_year.values(
            "related_order__related_products").count()

        return Overview(
            sale_by_day=affiliator_Transaction_by_day_amount,
            sale_by_month=affiliator_Transaction_by_month_amount,
            sale_by_year=affiliator_Transaction_by_year_amount,
            count_by_day=day_count,
            count_by_month=month_count,
            count_by_year=year_count,
        )

    @login_required
    def resolve_aff_top_products(self, info, aff_user_id):
        products = Transaction.objects.filter(
            related_order__related_affiliation__affiliator__user__id=aff_user_id).values("related_order__related_products")
        sorted_by_count_products = products.annotate(count=Count(
            "related_order__related_products")).order_by("-count")

        result = [
            TopProduct(Product.objects.get(id=item["related_order__related_products"]), item["count"]) for item in sorted_by_count_products
        ]
        return result

    @login_required
    def resolve_aff_top_categories(self, info, aff_user_id):
        categories = Transaction.objects.filter(
            related_order__related_affiliation__affiliator__user__id=aff_user_id).values("related_order__related_products__categories")
        sorted_by_count_categories = categories.annotate(count=Count(
            "related_order__related_products__categories")).order_by("-count")
        result = [
            TopCategory(Category.objects.get(id=item["related_order__related_products__categories"]), item["count"]) for item in sorted_by_count_categories
        ]
        return result
