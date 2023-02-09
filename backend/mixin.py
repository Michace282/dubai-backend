from django.db import models
from graphene_django.forms.mutation import DjangoModelFormMutation as DjangoModelFormMutationBase, \
    ClientIDMutation as ClientIDMutationBase
from graphene_django.types import ErrorType
import graphene
from graphql_relay import from_global_id


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class DjangoModelFormMutation(DjangoModelFormMutationBase):
    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        new_input = {}

        for (k, v) in input.items():
            try:
                new_input[k] = from_global_id(v)[1]
            except:
                new_input[k] = v

        kwargs = {"data": new_input}

        pk = input.pop("id", None)
        if pk:
            instance = cls._meta.model._default_manager.get(pk=from_global_id(pk)[1])
            kwargs["instance"] = instance
            kwargs["request"] = info.context

        return kwargs


class ClientIDMutation(ClientIDMutationBase):
    errors = graphene.List(ErrorType)

    class Meta:
        abstract = True
