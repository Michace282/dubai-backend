# Generated by Django 2.0.3 on 2021-02-14 12:27

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_basket_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Basket', 'verbose_name_plural': 'Baskets'},
        ),
        migrations.AddField(
            model_name='basket',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='basket',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='basket',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='basket',
            name='description',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='basket',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-Mail'),
        ),
        migrations.AddField(
            model_name='basket',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='First name'),
        ),
        migrations.AddField(
            model_name='basket',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name'),
        ),
        migrations.AddField(
            model_name='basket',
            name='pay',
            field=models.CharField(choices=[('Card', 'Card'), ('Delivery', 'Delivery')], default='Delivery', max_length=30, verbose_name='Pay'),
        ),
        migrations.AddField(
            model_name='basket',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='basket',
            name='postal_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='P.O. Box'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '350x500', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
