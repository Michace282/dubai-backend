from django.contrib import admin
from .models import Product, ProductSizeColor, ProductImage, Color, SizeChart, Size, Feedback, FeedbackImage, Basket, \
    ProductBasket, ProductSizeColorSize, ProductTypeSection
from django_summernote.widgets import SummernoteWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.urls import reverse
from django import forms
from django.template.loader import render_to_string
from django.forms.models import BaseInlineFormSet
import json
from django_summernote.admin import SummernoteModelAdmin

class SizeChartModelForm(forms.ModelForm):
    class Meta:
        model = SizeChart
        fields = '__all__'
        widgets = {
            'table': SummernoteWidget(attrs={'summernote': {'toolbar': ['table']}}),
        }


class SizeInline(admin.TabularInline):
    model = Size


@admin.register(SizeChart)
class SizeChartAdmin(admin.ModelAdmin):
    inlines = (SizeInline,)
    form = SizeChartModelForm


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


class BookInlineFormSet(BaseInlineFormSet):
    def save_new_objects(self, commit=True):
        saved_instances = super(BookInlineFormSet, self).save_new_objects(commit)
        if commit:
            pass
        return saved_instances

    def save_existing_objects(self, commit=True):
        saved_instances = super(BookInlineFormSet, self).save_existing_objects(commit)
        if commit:
            productsizecolor_set_size_element = self.data.getlist('productsizecolor_set-size-element[]', [])
            for element in productsizecolor_set_size_element:
                count = self.data.get(f'productsizecolor_set-size-input-{element}', 0)
                is_available = True if self.data.get(f'productsizecolor_set-size-checkbox-{element}', False) else False

                c_id, s_id = element.split('-')

                product_size_color_size = ProductSizeColorSize.objects.filter(product_size_color_id=int(c_id),
                                                                              id=int(s_id)).first()

                if product_size_color_size:
                    product_size_color_size.count = count
                    product_size_color_size.is_available = is_available
                    product_size_color_size.save()

        return saved_instances


class ProductSizeColorInline(admin.TabularInline):
    model = ProductSizeColor
    show_change_link = True
    formset = BookInlineFormSet
    exclude = ('sizes',)

    def render_inline_actions(self, obj=None):
        render = render_to_string('admin/render_inline_actions.html', {'obj': obj if obj else None})
        return mark_safe(render)

    render_inline_actions.short_description = 'Images'
    render_inline_actions.allow_tags = True

    def render_inline_actions_size(self, obj=None):
        render = render_to_string('admin/render_inline_actions_size.html', {'obj': obj if obj else None})
        return mark_safe(render)

    render_inline_actions_size.short_description = 'Size/Count/Is available'
    render_inline_actions_size.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = list(fields)
        if obj:
            fields.append('render_inline_actions')
            fields.append('render_inline_actions_size')
        return fields


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(ProductSizeColor)
class ProductSizeColorAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline,)

    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('__str__', 'status', 'product_type', 'profile_type', 'price','price_sale')
    list_filter = ('status', 'product_type', 'ladies_type', 'mens_type', 'accessories_type', 'dance_shoes_type','is_new')
    inlines = (ProductSizeColorInline,)
    autocomplete_fields = ('works_best_with',)
    search_fields = ('name', 'data', 'description', 'model_description')

    def profile_type(self, obj):
        if obj.product_type == 'ladies':
            return obj.get_ladies_type_display()
        if obj.product_type == 'mens':
            return obj.get_mens_type_display()
        if obj.product_type == 'accessories':
            return obj.get_accessories_type_display()
        if obj.product_type == 'dance_shoes':
            return obj.get_dance_shoes_type_display()
        return '-'

    fieldsets = (
        (None, {
            'fields': (
                ('status','is_new'),
                'article',
                ('name', 'product_type', 'ladies_type', 'mens_type', 'accessories_type', 'dance_shoes_type',),
                ('price','price_sale'),
                'description',
                'size_chart',
                'works_best_with',
                'video'
            )
        }),
    )

    class Media:
        js = ("js/product.js",)


class FeedbackImageInline(admin.StackedInline):
    model = FeedbackImage


@admin.register(ProductTypeSection)
class ProductTypeSectionAdmin(SummernoteModelAdmin):
    search_fields = ('product_type',)


    fieldsets = (
        (None, {
            'fields': (
                'product_type',
                'description',
            )
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    inlines = (FeedbackImageInline,)


class ProductBasketInline(admin.StackedInline):
    model = ProductBasket

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = (ProductBasketInline,)
    list_display = (
        'get_id', '__str__', 'get_count_productbasket', 'total_price', 'status', 'phone', 'country', 'city', 'address',
        'pay', 'guest', 'user')
    list_filter = ('status', 'pay')
    readonly_fields = ('code', 'guest', 'user')

    def get_id(self, obj):
        return str('{:09}'.format(obj.id))

    get_id.short_description = '№'

    def get_count_productbasket(self, obj):
        return obj.productbasket_set.count()

    get_id.short_description = 'Count'
