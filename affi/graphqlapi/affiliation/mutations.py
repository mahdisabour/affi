import graphene
from graphene import ObjectType
from graphql_jwt.decorators import login_required

from ...affiliation.models import Affiliation, Order
from ...user.models import Aff
from ...shop.models import Shop
from ...core.models import User


class RequestAffiliationUrl(graphene.Mutation):
    class Arguments:
        aff_user_id = graphene.Int()
        shop_id = graphene.Int()

    status = graphene.String()
    error = graphene.String()
    affiliation_url = graphene.String()

    @login_required
    def mutate(self, info, aff_user_id, shop_id):
        user = User.objects.get(id=aff_user_id)
        if user.role != "AFF":
            return RequestAffiliationUrl(status="Failed", error="User is not Affiliator")
        affiliator = Aff.objects.get(user__pk=aff_user_id)
        shop = Shop.objects.get(id=shop_id)
        affiliation = Affiliation.objects.filter(affiliator=affiliator, related_shop=shop) 
        if affiliation.exists():
            affiliation = affiliation.first()
        else:
            affiliation = Affiliation.objects.create(
                affiliator=affiliator,
                related_shop=shop
            )
        return RequestAffiliationUrl(status="Success", affiliation_url=affiliation.affiliation_url)


class CreateOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int()
        aff_id = graphene.Int()

    error = graphene.String()
    status = graphene.String()

    def mutate(self, info, order_id, aff_id):
        affiliation = Affiliation.objects.get(id=aff_id)
        if Order.objects.filter(base_order_id=order_id, related_affiliation=affiliation).exists():
            return CreateOrder(status="Failed", error="This Order has been created before")
        Order.objects.create(
            related_affiliation=affiliation,
            base_order_id=order_id
        )
        return CreateOrder(status="Success")
        

class AffiliationMutations(ObjectType):
    request_affiliation_url = RequestAffiliationUrl.Field()
    create_order = CreateOrder.Field()


