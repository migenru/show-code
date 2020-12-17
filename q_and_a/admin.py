from django.contrib import admin

from .models import Question, Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'content', 'question')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'content')
