from django.db import models
from backend.mixin import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem
from django.utils import timezone


class Gift(TimeStampedModel):
    class StatusType(DjangoChoices):
        published = ChoiceItem(label='Published', value='published')
        unpublished = ChoiceItem(label='Unpublished', value='unpublished')
        moderated = ChoiceItem(label='Moderated', value='moderated')

    name = models.CharField(verbose_name='Name', max_length=30)
    description = models.TextField(verbose_name='Description')
    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.published)

    published = models.DateTimeField(verbose_name='Published', default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Gift'
        verbose_name_plural = 'Gifts'
        ordering = ['-created_at']
