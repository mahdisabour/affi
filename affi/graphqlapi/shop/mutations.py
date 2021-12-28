import graphene
import graphene_django
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required


from ..core.types import CreateUserInputType
from ...core.models import User
from ...shop.models import Shop, ShopRate
from ...user.models import Aff
from ...product.models import Product
from ..core.types import UserUpdateInputType
from .types import ShopUpdateInputType, ProductVisibility


class CreateShop(graphene.Mutation):
    class Arguments:
        user_data = CreateUserInputType(required=True)
        url = graphene.String(required=True)

    status = graphene.String()

    def mutate(self, info, user_data, **kwargs):
        user = User(
            phone_number=user_data.get("phone_number"),
            email=user_data.get("email_address"),
            name=user_data.get("name")
        )
        user.set_password(user_data.get("password"))
        user.save()

        Shop.objects.create(
            user=user,
            url=kwargs.get("url")
        )
        return CreateShop(status="success")


class UpdateShop(graphene.Mutation):
    class Arguments:
        shop_data = ShopUpdateInputType()
        user_data = UserUpdateInputType()

    status = graphene.String()

    @login_required
    def mutate(self, info, shop_data, user_data):
        user = info.context.user
        # update user values
        if user_data:
            for key, val in user_data.items():
                if val:
                    setattr(user, key, val)
            user.save()
        try:
            shop = Shop.objects.get(user__phone_number=user.phone_number)
        except:
            return UpdateShop(status="fail, you are not shop")
        # update shop values
        if shop_data:
            for key, val in shop_data.items():
                if val:
                    setattr(shop, key, val)
            shop.save()

        return UpdateShop(status="success")


class RateShop(graphene.Mutation):
    class Arguments:
        rate = graphene.Int(required=True)
        shop_id = graphene.Int(required=True)

    status = graphene.String()

    @login_required
    def mutate(self, info, rate, shop_id):
        if Aff.objects.filter(user__phone_number=info.context.user.phone_number).exists():
            aff = Aff.objects.filter(
                user__phone_number=info.context.user.phone_number).first()
        else:
            return RateShop("you are not aff user")
        shop = Shop.objects.get(id=shop_id)
        if ShopRate.objects.filter(aff=aff, shop=shop).exists():
            shop_rate = ShopRate.objects.get(aff=aff, shop=shop)
            shop_rate.rate = rate
            shop_rate.save()
        else:
            ShopRate.objects.create(
                aff=aff,
                shop=shop,
                rate=rate
            )
        return RateShop(status="success")


class UpdateShopProductsAffiliationRate(graphene.Mutation):
    class Arguments:
        affiliation_rate = graphene.Float()

    status = graphene.String()

    @login_required
    def mutate(self, info, affiliation_rate):
        shop = Shop.objects.get(user=info.context.user)
        shop.products.all().update(affiliate_rate=affiliation_rate)
        return UpdateShopProductsAffiliationRate(status="Success")


class ShopProductManager(graphene.Mutation):
    class Arguments:
        shop_user_id = graphene.Int()
        products = graphene.List(ProductVisibility)

    status = graphene.String()

    @login_required
    def mutate(self, info, shop_user_id, products):
        shop_user = Shop.objects.get(user__id=shop_user_id).user
        if shop_user != info.context.user:
            ShopProductManager(status="you have not access")
        for product in products:
            product_obj = Product.objects.get(id=product["id"])
            product_obj.visibility = product["visibility"]
            product_obj.save()
        return ShopProductManager(status="Success")


class GetShopKeys(graphene.Mutation):
    class Arguments:
        api_consumer_key = graphene.String()
        api_secret_key = graphene.String()

    status = graphene.String()

    @login_required
    def mutate(self, info, api_consumer_key, api_secret_key):
        shop = Shop.objects.get(user=info.context.user)
        if not shop:
            return GetShopKeys(status="you have not access")
        shop.api_consumer_key = api_consumer_key
        shop.api_secret_key = api_secret_key
        shop.save()
        return GetShopKeys(status="Success")


class ShopMutation(graphene.ObjectType):
    create_shop = CreateShop.Field()
    rate_shop = RateShop.Field()
    update_shop = UpdateShop.Field()
    update_shop_products_affiliation_rate = UpdateShopProductsAffiliationRate.Field()
    shop_product_manager = ShopProductManager.Field()
    get_shop_keys = GetShopKeys.Field()
