import graphene
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from .models import *
from django.conf import settings


class StockType(DjangoObjectType):
    image_cropping = graphene.String()

    def resolve_image_cropping(self, info):
        if self.image:
            return f'{settings.BACKEND_URL[:-1]}{self.image_cropping}'
        return None

    class Meta:
        model = Stock
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(status=Stock.StatusType.published)


class Query(graphene.ObjectType):
    stock_list = DjangoConnectionField(StockType)
