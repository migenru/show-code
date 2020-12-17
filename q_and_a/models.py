from django.db import models
from core.models import NodeModel


class Question(NodeModel):
    pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(NodeModel):
    question = models.OneToOneField(Question, on_delete=models.DO_NOTHING, verbose_name='Вопрос', related_name='answer')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'