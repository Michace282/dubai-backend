from django.db import models
from django.db.models import When, Case
from djchoices import DjangoChoices, ChoiceItem
from backend.mixin import TimeStampedModel
from colorfield.fields import ColorField
from account.models import Guest, Code
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
from image_cropping.utils import get_backend
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


class ProductTypeSection(TimeStampedModel):
    class Type(DjangoChoices):
        ladies = ChoiceItem(label='Ladies', value='ladies')
        mens = ChoiceItem(label='Mens', value='mens')
        accessories = ChoiceItem(label='Accessories', value='Accessories')
        dance_shoes = ChoiceItem(label='Dance shoes', value='Dance shoes')
        leotards = ChoiceItem(label='Leotards', value='Leotards')
        body = ChoiceItem(label='Body(old)', value='Body(old)')
        blouses = ChoiceItem(label='Blouses', value='Blouses')
        skirts = ChoiceItem(label='Skirts', value='Skirts')
        dresses = ChoiceItem(label='Dresses', value='Dresses')
        pants = ChoiceItem(label='Pants', value='Pants')
        trousers = ChoiceItem(label='Trousers(old)', value='Trousers(old)')
        jumpsuits = ChoiceItem(label='Jumpsuits', value='Jumpsuits')
        tops = ChoiceItem(label='Tops', value='Tops')
        shorts = ChoiceItem(label='Shorts', value='Shorts')
        trousers = ChoiceItem(label='Trousers', value='Trousers')
        waistcoasts = ChoiceItem(label='Waistcoasts', value='Waistcoasts')
        shirts = ChoiceItem(label='Shirts', value='Shirts')
        t_shirts = ChoiceItem(label='T-shirts', value='T-shirts')
        shoe_accessories = ChoiceItem(label='Shoe accessories', value='Shoe accessories')
        bags = ChoiceItem(label='Bags', value='Bags')
        ladies_accessories = ChoiceItem(label='Ladies accessories', value='Ladies accessories')
        ladies = ChoiceItem(label='Ladies', value='Ladies')
        mens = ChoiceItem(label='Mens', value='Mens')
    product_type = models.CharField(verbose_name='Product type',
                                    max_length=30,
                                    choices=Type.choices)
    description = models.TextField(verbose_name='Description')

    class Meta:
        unique_together = ('product_type')


    def __str__(self):
        return self.product_type

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Type Section'
        verbose_name_plural = 'Product Types Section'


class SizeChart(TimeStampedModel):
    name = models.CharField(verbose_name='Name size chart', max_length=30)
    table = models.TextField(verbose_name='Table')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Size Chart'
        verbose_name_plural = 'Size Charts'


class Size(TimeStampedModel):
    class SizeType(DjangoChoices):
        xs = ChoiceItem(label='xs', value='xs')
        s = ChoiceItem(label='s', value='s')
        m = ChoiceItem(label='m', value='m')
        l = ChoiceItem(label='l', value='l')
        xl = ChoiceItem(label='xl', value='xl')
        xxl = ChoiceItem(label='xxl', value='xxl')
        xxxl = ChoiceItem(label='xxxl', value='xxxl')
        xxxxl = ChoiceItem(label='xxxxl', value='xxxxl')

    chart = models.ForeignKey(SizeChart, verbose_name='Chart', on_delete=models.CASCADE)
    name = models.TextField(verbose_name='Name size', max_length=30)
    size = models.CharField(verbose_name='Type size', max_length=30, choices=SizeType.choices, default=SizeType.xs)

    def __str__(self):
        return f'{self.name}, ({str(self.chart)})'

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'


class Color(TimeStampedModel):
    name = models.CharField(verbose_name='Name color', max_length=30)
    description = models.CharField(verbose_name='Description', max_length=30, blank=True, null=True)
    color = ColorField(verbose_name='Color', default='#FFFFFF')
    image = models.ImageField(verbose_name='Image(64x64)',
                              help_text='If an image is uploaded, it will be displayed in colors.',
                              blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'


class Product(TimeStampedModel):
    class StatusType(DjangoChoices):
        published = ChoiceItem(label='Published', value='published')
        unpublished = ChoiceItem(label='Unpublished', value='unpublished')
        moderated = ChoiceItem(label='Moderated', value='moderated')

    class ProductType(DjangoChoices):
        ladies = ChoiceItem(label='Ladies', value='ladies')
        mens = ChoiceItem(label='Mens', value='mens')
        accessories = ChoiceItem(label='Accessories', value='accessories')
        dance_shoes = ChoiceItem(label='Dance shoes', value='dance_shoes')
        performance_costumes = ChoiceItem(label='Performance costumes', value='performance_costumes')

    class LadiesType(DjangoChoices):
        leotards = ChoiceItem(label='Leotards', value='leotards')
        body = ChoiceItem(label='Body(old)', value='body')
        blouses = ChoiceItem(label='Blouses', value='blouses')
        skirts = ChoiceItem(label='Skirts', value='skirts')
        dresses = ChoiceItem(label='Dresses', value='dresses')
        pants = ChoiceItem(label='Pants', value='pants')
        trousers = ChoiceItem(label='Trousers(old)', value='trousers')
        jumpsuits = ChoiceItem(label='Jumpsuits', value='jumpsuits')
        tops = ChoiceItem(label='Tops', value='tops')
        shorts = ChoiceItem(label='Shorts', value='shorts')

    class MensType(DjangoChoices):
        trousers = ChoiceItem(label='Trousers', value='trousers')
        waistcoasts = ChoiceItem(label='Waistcoasts', value='waistcoasts')
        shirts = ChoiceItem(label='Shirts', value='shirts')
        t_shirts = ChoiceItem(label='T-shirts', value='t_shirts')

    class AccessoriesType(DjangoChoices):
        shoe_accessories = ChoiceItem(label='Shoe accessories', value='shoe_accessories')
        bags = ChoiceItem(label='Bags', value='bags')
        ladies_accessories = ChoiceItem(label='Ladies accessories', value='ladies_accessories')

    class DanceShoesType(DjangoChoices):
        ladies = ChoiceItem(label='Ladies', value='ladies')
        mens = ChoiceItem(label='Mens', value='mens')

    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.published)

    name = models.CharField(verbose_name='Model name', max_length=30)
    product_type = models.CharField(verbose_name='Product type',
                                    max_length=30,
                                    choices=ProductType.choices)

    ladies_type = models.CharField(verbose_name='Ladies type',
                                   max_length=30,
                                   choices=LadiesType.choices,
                                   blank=True,
                                   null=True)

    mens_type = models.CharField(verbose_name='Mens type',
                                 max_length=30,
                                 choices=MensType.choices,
                                 blank=True,
                                 null=True)

    accessories_type = models.CharField(verbose_name='Accessories type',
                                        choices=AccessoriesType.choices,
                                        max_length=30,
                                        blank=True,
                                        null=True)

    dance_shoes_type = models.CharField(verbose_name='Dance shoes type',
                                        max_length=30,
                                        choices=DanceShoesType.choices, blank=True,
                                        null=True)

    article = models.CharField(verbose_name='Article', max_length=30)
    price = models.PositiveIntegerField(verbose_name='Price')
    price_sale = models.PositiveIntegerField(verbose_name='Price Old')
    is_new = models.BooleanField(verbose_name='Is New')
    video = models.FileField(upload_to='product/video',null=True, blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    description = models.TextField(verbose_name='Description')
    model_description = models.TextField(verbose_name='Model description', blank=True, null=True)
    size_chart = models.ForeignKey(SizeChart, verbose_name='Size Chart', on_delete=models.CASCADE,
                                   help_text='If you change the size table, the old dimensions will be deleted.')

    data = models.TextField(blank=True, null=True)
    works_best_with = models.ManyToManyField('product.Product', verbose_name='Works best with', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'





class ProductSizeColor(TimeStampedModel):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='Color', on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, verbose_name='Size')
    is_available = models.BooleanField(verbose_name='Is it available?', default=True)

    class Meta:
        unique_together = ('product', 'color')

    def __str__(self):
        return f'{str(self.color)}'

    class Meta:
        verbose_name = 'Product color'
        verbose_name_plural = 'Product colors'


class ProductSizeColorSize(TimeStampedModel):
    product_size_color = models.ForeignKey(ProductSizeColor, verbose_name='Product color', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, verbose_name='Size', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Count', default=0)
    is_available = models.BooleanField(verbose_name='Is it available?', default=True)

    class Meta:
        unique_together = ('product_size_color', 'size')

    def __str__(self):
        return f'{str(self.product_size_color)} + {str(self.size)}'

    class Meta:
        verbose_name = 'Product color size'
        verbose_name_plural = 'Product color sizes'


@receiver(post_save, sender=Product, dispatch_uid="update_product")
def update_product(sender, instance, **kwargs):
    if instance.size_chart:

        first_product_size_color_size = ProductSizeColorSize.objects.filter(
            product_size_color__product=instance).first()

        if first_product_size_color_size:
            if first_product_size_color_size.size.chart != instance.size_chart:
                ProductSizeColorSize.objects.filter(product_size_color__product=instance).delete()

                for color in ProductSizeColor.objects.filter(product=instance):
                    for size in instance.size_chart.size_set.all():
                        if not ProductSizeColorSize.objects.filter(size=size, product_size_color=color).exists():
                            ProductSizeColorSize.objects.create(size=size, product_size_color=color)


@receiver(post_save, sender=ProductSizeColor, dispatch_uid="update_product_size_color")
def update_product_size_color(sender, instance, **kwargs):
    if instance.product.size_chart:
        for size in instance.product.size_chart.size_set.all():
            if not ProductSizeColorSize.objects.filter(size=size, product_size_color=instance).exists():
                ProductSizeColorSize.objects.create(size=size, product_size_color=instance)


class ProductImage(TimeStampedModel):
    product_size_color = models.ForeignKey(ProductSizeColor, verbose_name='Product Size Color',
                                           on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image', upload_to='product/image')
    cropping = ImageRatioField('image', '350x500')

    def __str__(self):
        return str(self.product_size_color)

    @property
    def image_cropping(self):
        if self.image:
            return get_backend().get_thumbnail_url(self.image, {
                'box': self.cropping,
                'size': (350, 500),
                'crop': True,
                'detail': True,
            })
            return
        else:
            return ''

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'


class ProductWishlist(TimeStampedModel):
    guest = models.ForeignKey(Guest, verbose_name='Guest', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)


class Basket(TimeStampedModel):
    class PayType(DjangoChoices):
        card = ChoiceItem(label='Card', value='card')
        delivery = ChoiceItem(label='Delivery', value='delivery')

    class StatusType(DjangoChoices):
        completed = ChoiceItem(label='Completed', value='completed')
        sent = ChoiceItem(label='Sent', value='sent')
        processing = ChoiceItem(label='Processing', value='processing')
        new = ChoiceItem(label='New', value='new')
        rejected = ChoiceItem(label='rejected', value='rejected')

    first_name = models.CharField(verbose_name='First name', max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name='Last name', max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name='Address', max_length=255, blank=True, null=True)
    postal_code = models.CharField(verbose_name='P.O. Box', max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name='City', max_length=255, blank=True, null=True)
    country = models.CharField(verbose_name='Country', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name='Phone', max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name='E-Mail', blank=True, null=True)
    description = models.EmailField(verbose_name='Description', blank=True, null=True)

    code = models.ForeignKey(Code, verbose_name='Code', on_delete=models.CASCADE, blank=True, null=True)
    discount = models.IntegerField(verbose_name='Discount', default=0)
    total_price = models.IntegerField(verbose_name='Total price', default=0, editable=True)
    guest = models.ForeignKey(Guest, verbose_name='Guest', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.new)

    is_completed = models.BooleanField(verbose_name='Is completed', default=False, editable=True)

    code_delivery = models.CharField(verbose_name='Code - delivery', max_length=255, blank=True, null=True)

    pay = models.CharField(verbose_name='Pay',
                           max_length=30,
                           choices=PayType.choices,
                           default=PayType.delivery)

    def __str__(self):
        if self.first_name or self.last_name:
            return str(self.first_name) + ' ' + str(self.last_name)
        return super().__str__()

    class Meta:
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'


@receiver(post_save, sender=Basket, dispatch_uid="update_basket")
def update_basket(sender, instance, created, **kwargs):
    if created:
        for productbasket in instance.productbasket_set.all():
            product_size_color_size = ProductSizeColorSize.objects.filter(
                product_size_color__product=productbasket.product,
                product_size_color__color=productbasket.color,
                size=productbasket.size).first()

            if product_size_color_size:
                product_size_color_size.count = product_size_color_size.count - productbasket.count if product_size_color_size.count - productbasket.count > 0 else 0
                product_size_color_size.save()


class ProductBasket(TimeStampedModel):
    basket = models.ForeignKey(Basket, verbose_name='Basket', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Price')
    count = models.PositiveIntegerField(verbose_name='Count')
    size = models.ForeignKey(Size, verbose_name='Size', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='Color', on_delete=models.CASCADE)


class Feedback(TimeStampedModel):
    class StatusType(DjangoChoices):
        published = ChoiceItem(label='Published', value='published')
        unpublished = ChoiceItem(label='Unpublished', value='unpublished')
        moderated = ChoiceItem(label='Moderated', value='moderated')

    class StarType(DjangoChoices):
        star1 = ChoiceItem(label='star1', value=1)
        star2 = ChoiceItem(label='star2', value=2)
        star3 = ChoiceItem(label='star3', value=3)
        star4 = ChoiceItem(label='star4', value=4)
        star5 = ChoiceItem(label='star5', value=5)

    guest = models.ForeignKey(Guest, verbose_name='Guest', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, verbose_name='Size', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='Color', on_delete=models.CASCADE)

    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.moderated)

    star = models.IntegerField(verbose_name='Star',
                               choices=StarType.choices)

    text = models.TextField(verbose_name='Text')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        unique_together = ('product', 'color',)


class FeedbackImage(TimeStampedModel):
    feedback = models.ForeignKey(Feedback, verbose_name='Feedback',
                                 on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image', upload_to='feedback/image')

    def __str__(self):
        return str(self.feedback)

    class Meta:
        verbose_name = 'Feedback image'
        verbose_name_plural = 'Feedback images'
