from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ('__str__', 'status', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}
