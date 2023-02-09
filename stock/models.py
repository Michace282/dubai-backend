from django.db import models
from backend.mixin import TimeStampedModel
from image_cropping import ImageRatioField
from djchoices import DjangoChoices, ChoiceItem
from product.models import Product
from django.utils import timezone
from image_cropping.utils import get_backend


class Stock(TimeStampedModel):
    class StatusType(DjangoChoices):
        published = ChoiceItem(label='Published', value='published')
        unpublished = ChoiceItem(label='Unpublished', value='unpublished')
        moderated = ChoiceItem(label='Moderated', value='moderated')

    name = models.CharField(verbose_name='Name', max_length=30)
    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.published)

    name_product = models.CharField(verbose_name='Name product', max_length=30, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(verbose_name='Image')
    cropping = ImageRatioField('image', '1300x702')
    published = models.DateTimeField(verbose_name='Published', default=timezone.now)

    @property
    def image_cropping(self):
        if self.image:
            return get_backend().get_thumbnail_url(self.image, {
                'box': self.cropping,
                'size': (1300, 702),
                'crop': True,
                'detail': True,
            })
            return
        else:
            return ''

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ('published',)
