from django.db import models

class HomeCategory(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Home Category'
        verbose_name_plural = 'Home Categories Section'