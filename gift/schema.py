import graphene
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from .models import *
from django.conf import settings


class GiftType(DjangoObjectType):
    class Meta:
        model = Gift
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(status=Gift.StatusType.published)


class Query(graphene.ObjectType):
    gift_list = DjangoConnectionField(GiftType)
    gift_new_detail = graphene.Field(GiftType)

    def resolve_gift_new_detail(self, info):
        return Gift.objects.first()
