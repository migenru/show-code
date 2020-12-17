from django.contrib import admin

from .models import TagArticle, TypeArticle, Article, TermArticle, Comment


admin.site.register(TypeArticle)

def make_published(modeladmin, request, queryset):
    queryset.update(status='P')

make_published.short_description = "Установить статус 'Published'"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author' ,'status')
    list_filter = ('title', 'type', 'author', 'status')
    search_fields = ('title', 'author', 'content')
    actions = [make_published]


admin.site.register(Article, ArticleAdmin)


@admin.register(TagArticle)
class TagArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TermArticle)
class TermArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'is_active')
    list_filter = ('is_active', 'created', 'update')
    search_fields = ('name', 'email', 'content')