import graphene
from graphene_django import DjangoObjectType
from .models import HomeCategory

class HomeCategoryType(DjangoObjectType):
    class Meta:
        model = HomeCategory
        fields = ('id', 'status', 'name', 'image', 'link')

class Query(graphene.ObjectType):
    homeCategories = graphene.List(HomeCategoryType)

    def resolve_homeCategories(self, info, **kwargs):
        return HomeCategory.objects.filter(status='active').all()

schema = graphene.Schema(query=Query)
