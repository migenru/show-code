from django.db import models

from core.models import NodeModel, Term


class TagArticle(Term):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class TermArticle(Term):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    def __str__(self):
        if self.parent == None:
            return f'{self.name}'
        else:
            return f'{self.parent} > {self.name}'

    class Meta:
        verbose_name = 'Раздел сайта'
        verbose_name_plural = 'Разделы сайта'


class TypeArticle(models.Model):
    name = models.CharField(verbose_name='Название типа', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание типа', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип записи'
        verbose_name_plural = 'Типы записей'


class Article(NodeModel):
    image = models.ImageField('Cover post', upload_to='blog/%Y/%m/$d', blank=True)
    tag = models.ManyToManyField(TagArticle, verbose_name='Тег', blank=True)
    term = models.ManyToManyField(TermArticle, verbose_name='Раздел записи', blank=True)
    type = models.ForeignKey(TypeArticle, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField()
    content = models.TextField(verbose_name='Текст комментария')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Комментарий от {self.name} к статье {self.article}'
