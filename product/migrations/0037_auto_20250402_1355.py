from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('product', '0036_product_video'),  # Adjust based on your previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='kids_dancewear_type',
            field=models.CharField(max_length=50, null=True, blank=True),  # Adjust field type as per your model
        ),
        # Other operations...
    ]