import graphene

from .core.schema import CoreQuery
from .shop.schema import ShopQuery
from .category.schema import CategoryQuery
from .product.schema import ProductQuery
from .user.schema import UserQuery
from .financial.schema import FinancialQuery

from .core.mutations import CoreMutation


class Query(
    ShopQuery,
    UserQuery,
    CoreQuery,
    CategoryQuery,
    ProductQuery,
    FinancialQuery,
    graphene.ObjectType,
):
    pass


class Mutation(
    CoreMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
