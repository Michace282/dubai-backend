# Generated by Django 2.0.3 on 2021-02-02 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_product_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productsizecolor',
            name='size',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product_size_color',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.ProductSizeColor', verbose_name='Product Size Color'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsizecolor',
            name='sizes',
            field=models.ManyToManyField(to='product.Size', verbose_name='Size'),
        ),
    ]