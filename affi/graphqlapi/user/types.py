from graphene import InputObjectType
import graphene
from graphene_django import DjangoObjectType
from graphene import relay, InputObjectType
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required

from ...user.models import Aff


class PlainTextNode(relay.Node):
    class Meta:
        name = 'userNode'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def from_global_id(global_id):
        return global_id.split(':')


class Overview(graphene.ObjectType):
    sale_by_day = graphene.Int()
    sale_by_month = graphene.Int()
    sale_by_year = graphene.Int()
    count_by_day = graphene.Int()
    count_by_month = graphene.Int()
    count_by_year = graphene.Int()



class AffNode(DjangoObjectType):
    class Meta:
        model = Aff
        interfaces = (PlainTextNode, )
        filter_fields = ['id', ]
        filter_order_by = True

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset


class AffUpdateInputType(InputObjectType):
    age = graphene.Int()
    birth_data = graphene.Date()
    national_code = graphene.String()
