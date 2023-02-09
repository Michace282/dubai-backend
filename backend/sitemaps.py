from django.contrib import sitemaps
from product.models import Product
from product.schema import ProductType
from graphql_relay import to_global_id


class HomeSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'catalog',
            'about-us',
            'page/terms_condition',
            'page/privacy_policy',
            'returns',
            'contacts',
            'payment',
            '/',
        ]

    def location(self, item):
        if item == '/':
            return f'/'
        return f'/{item}/'


class ProductSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(status=Product.StatusType.published)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/product/{to_global_id(ProductType._meta.name, obj.id)}/'
