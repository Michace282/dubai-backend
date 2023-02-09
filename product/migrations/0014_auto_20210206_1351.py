# Generated by Django 2.0.3 on 2021-02-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20210205_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='star',
            field=models.IntegerField(choices=[(1, 'star1'), (2, 'star2'), (3, 'star3'), (4, 'star4'), (5, 'star5')], max_length=30, verbose_name='Star'),
        ),
    ]
