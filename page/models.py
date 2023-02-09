from django.db import models
from backend.mixin import TimeStampedModel
from djchoices import DjangoChoices, ChoiceItem


class Page(TimeStampedModel):
    class StatusType(DjangoChoices):
        published = ChoiceItem(label='Published', value='published')
        unpublished = ChoiceItem(label='Unpublished', value='unpublished')
        moderated = ChoiceItem(label='Moderated', value='moderated')

    name = models.CharField(verbose_name='Name page', max_length=30)
    slug = models.SlugField(verbose_name='Slug')
    text = models.TextField(verbose_name='Text')
    status = models.CharField(verbose_name='Status',
                              max_length=30,
                              choices=StatusType.choices,
                              default=StatusType.published)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
