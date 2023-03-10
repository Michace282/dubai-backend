# Generated by Django 2.0.3 on 2021-02-18 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20210218_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size_chart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.SizeChart', verbose_name='Size Chart'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(choices=[('xs', 'xs'), ('s', 's'), ('m', 'm'), ('l', 'l'), ('xl', 'xl'), ('xxl', 'xxl'), ('xxxl', 'xxxl'), ('xxxxl', 'xxxxl')], default='xs', max_length=30, verbose_name='Type size'),
        ),
    ]
