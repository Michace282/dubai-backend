from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import Stock


@admin.register(Stock)
class StockAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('__str__', 'status', 'product', 'published')
