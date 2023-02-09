from graphene_django.forms.converter import convert_form_field
import graphene
from django import forms
import django_filters


class ArrayFieldForm(forms.Field):
    pass


class ArrayFilter(django_filters.Filter):
    field_class = ArrayFieldForm


@convert_form_field.register(ArrayFieldForm)
def convert_form_field_to_boolean(field):
    return graphene.List(graphene.String)
