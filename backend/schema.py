import graphene
from graphene_django.debug import DjangoDebug
from product.schema import Query as ProductQuery, Mutation as ProductMutation
from stock.schema import Query as StockQuery
from page.schema import Query as PageQuery
from gift.schema import Query as GiftQuery
from account.schema import Query as AccountQuery, Mutation as AccountMutation


class Mutation(
    ProductMutation,
    AccountMutation,
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Query(
    GiftQuery,
    ProductQuery,
    PageQuery,
    StockQuery,
    AccountQuery,
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
