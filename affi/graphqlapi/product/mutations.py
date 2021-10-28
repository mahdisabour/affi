import graphene
from graphql_jwt.decorators import login_required

from affi import product

from ...shop.models import Shop
from ...product.models import Product

class UpdateProductAffiliationRate(graphene.Mutation):
    class Arguments:
        affiliation_rate = graphene.Float()
        product_id = graphene.Int()

    status = graphene.String()

    def mutate(self, info, affiliation_rate, product_id):
        shop = Shop.objects.get(user=info.context.user)
        product = Product.objects.get(related_shop=shop, id=product_id)
        product.affiliate_rate = affiliation_rate
        product.save()
        return UpdateProductAffiliationRate(status="Success")
    

class ProductMutations(graphene.ObjectType):
    update_product_affiliation_rate = UpdateProductAffiliationRate.Field()
    