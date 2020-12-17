from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Term(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        abstract = True


class NodeModel(TimeStampedModel):
    STATUS = [
        ('D', 'Draft'),
        ('P', 'Published'),
        ('T', 'Trash'),
    ]
    title = models.CharField(verbose_name='Название', max_length=200)
    content = models.TextField(verbose_name='Содержимое', blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', choices=STATUS, max_length=1, default='D')

    class Meta:
        abstract = True
