# Generated by Django 2.0.3 on 2022-08-17 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_product_isnew'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_sale',
            field=models.IntegerField(default=0, verbose_name='Sale Price')
        ),
    ]
