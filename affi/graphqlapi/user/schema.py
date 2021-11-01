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
from ...core.models import User
from ...financial.models import Transaction
from ...product.models import Product
from ...category.models import Category

from ..product.types import TopProduct
from ..category.types import TopCategory


class UserQuery(ObjectType):
    all_aff = DjangoFilterConnectionField(AffNode)
    overview = graphene.Field(Overview, user_id=graphene.Int())
    top_products = graphene.Field(TopProduct, user_id=graphene.Int())
    top_categories = graphene.Field(TopCategory, user_id=graphene.Int())

    @login_required
    def resolve_overview(self, info, user_id):
        user = info.context.user
        days = [1, 30, 365]
        transactions = {}
        if user.role in ["AFF", "ADMIN"]:
            transactions = {day: Transaction.objects.affiliator_transactions(
                user_id=user_id, days=day) for day in days}
            transactions_amount = {
                day: transaction.aggregate(
                    Sum('amount'))["amount__sum"] for day, transaction in transactions.items()
            }

        elif user.role in ["SHOP", "ADMIN"]:
            transactions = {day: Transaction.objects.shop_transactions(
                user_id=user_id, days=day) for day in days}
            transactions_amount = {}
            for day, translation in transactions.items():
                print(day)
                print(translation)
                price = Transaction.objects.shop_products_price(
                    user_id=user_id, days=day)
                price_affiliate = translation.aggregate(Sum('amount'))[
                    "amount__sum"]
                if price or price_affiliate:
                    transactions_amount[day] = price - price_affiliate
                else:
                    transactions_amount[day] = 0

        transactions_count = {day: transaction.values(
            "related_order__related_products").count() for day, transaction in transactions.items()}

        return Overview(
            sale_by_day=transactions_amount[1] if transactions_amount[1] else 0,
            sale_by_month=transactions_amount[30] if transactions_amount[30] else 0,
            sale_by_year=transactions_amount[365] if transactions_amount[365] else 0,
            count_by_day=transactions_count[1] if transactions_count[1] else 0,
            count_by_month=transactions_count[30] if transactions_count[30] else 0,
            count_by_year=transactions_count[365] if transactions_count[365] else 0,
        )

    @login_required
    def resolve_top_products(self, info, user_id):
        user = User.objects.get(id=user_id)

        if user.role in ["AFF", "ADMIN"]:
            aff_products = Transaction.objects.aff_products(user_id=user_id)
            products_detail = aff_products.annotate(
                count=Count("id"), sum=Sum("price")).order_by("-count")
            amount = [int(product.sum * product.affiliate_rate / 100)
                      for product in products_detail]
        if user.role in ["SHOP", "ADMIN"]:
            shop_products = Transaction.objects.shop_products(user_id=user_id)
            products_detail = shop_products.annotate(
                count=Count("id"), sum=Sum("price")).order_by("-count")
            amount = [product.sum - int(product.sum * product.affiliate_rate / 100)
                      for product in products_detail]

        name = [product.name for product in products_detail]
        count = [product.count for product in products_detail]
        values = [[_count, _amount] for _count, _amount in zip(count, amount)]

        return TopProduct(
            labels=name,
            values=values
        )

    @login_required
    def resolve_top_categories(self, info, user_id):
        user = User.objects.get(id=user_id)

        if user.role in ["AFF", "ADMIN"]:
            categories = Transaction.objects.filter(
                related_order__related_affiliation__affiliator__user__id=user_id).values("related_order__related_products__categories")

        if user.role in ["SHOP", "ADMIN"]:
            categories = Transaction.objects.filter(
                related_order__related_affiliation__related_shop__user__id=user_id).values("related_order__related_products__categories")

        # categories_detail = categories.annotate(count=Count(
        #     "related_order__related_products__categories"), shop_profit=Sum("related_order__related_products__price"), amount=Sum("amount")).order_by("-count")

        categories_detail = categories.annotate(count=Count(
            "related_order__related_products__categories")).order_by("-count")

        labels = [Category.objects.get(
            id=item["related_order__related_products__categories"]).name for item in categories_detail]
        values = [[item["count"]] for item in categories_detail]

        return TopCategory(
            labels=labels,
            values=values
        )
