import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from .models import *


class PageType(DjangoObjectType):
    class Meta:
        model = Page
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    page_detail = graphene.Field(PageType, slug=graphene.String())

    def resolve_page_detail(self, info, slug):
        return Page.objects.filter(slug=slug, status=Page.StatusType.published).first()
