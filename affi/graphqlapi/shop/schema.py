from django.db.models import Sum, Count

import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

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
    shop_overview = graphene.Field(Overview, shop_user_id=graphene.Int())
    shop_top_products = graphene.List(TopProduct, shop_user_id=graphene.Int())
    shop_top_categories = graphene.List(TopCategory, shop_user_id=graphene.Int())

    def resolve_shop(self, info, id):
        return Shop.objects.filter(pk=id).first()

    @login_required
    def resolve_shop_overview(self, info, shop_user_id):
        shop_Transaction_by_day = Transaction.objects.shop_transactions(
            user_id=shop_user_id, days=1)
        shop_Transaction_by_day_amount = shop_Transaction_by_day.aggregate(
            Sum('amount'))["amount__sum"]
        day_count = shop_Transaction_by_day.values(
            "related_order__related_products").count()

        shop_Transaction_by_month = Transaction.objects.shop_transactions(
            user_id=shop_user_id, days=30)
        shop_Transaction_by_month_amount = shop_Transaction_by_month.aggregate(
            Sum('amount'))["amount__sum"]
        month_count = shop_Transaction_by_month.values(
            "related_order__related_products").count()

        shop_Transaction_by_year = Transaction.objects.shop_transactions(
            user_id=shop_user_id, days=365)
        shop_Transaction_by_year_amount = shop_Transaction_by_year.aggregate(
            Sum('amount'))["amount__sum"]
        year_count = shop_Transaction_by_year.values(
            "related_order__related_products").count()

        return Overview(
            sale_by_day=shop_Transaction_by_day_amount,
            sale_by_month=shop_Transaction_by_month_amount,
            sale_by_year=shop_Transaction_by_year_amount,
            count_by_day=day_count,
            count_by_month=month_count,
            count_by_year=year_count,
        )

    @login_required
    def resolve_shop_top_products(self, info, shop_user_id):
        products = Transaction.objects.filter(
            related_order__related_affiliation__related_shop__user__id=shop_user_id).values("related_order__related_products")
        sorted_by_count_products = products.annotate(count=Count(
            "related_order__related_products")).order_by("-count")
        result = [
            TopProduct(Product.objects.get(id=item["related_order__related_products"]), item["count"]) for item in sorted_by_count_products
        ]
        return result


    @login_required
    def resolve_shop_top_categories(self, info, shop_user_id):
        categories = Transaction.objects.filter(
            related_order__related_affiliation__related_shop__user__id=shop_user_id).values("related_order__related_products__categories")
        sorted_by_count_categories = categories.annotate(count=Count(
            "related_order__related_products__categories")).order_by("-count")
        result = [
            TopCategory(Category.objects.get(id=item["related_order__related_products__categories"]), item["count"]) for item in sorted_by_count_categories
        ]
        return result