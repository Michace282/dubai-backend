from django.contrib import admin
from .models import Gift


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'status', 'published')
    list_filter = ('status',)
