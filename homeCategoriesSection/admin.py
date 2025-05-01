from django.contrib import admin
from .models import HomeCategory

@admin.register(HomeCategory)
class HomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'link')
    list_filter = ('status',)
    search_fields = ('name',)