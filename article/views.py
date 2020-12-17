from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Article, TypeArticle
from .forms import CommentForm


def index(request, slug):
    page = Article.objects.get(slug=slug)
    context = {
        'page': page,
    }
    return render(request, 'article/base_page.html', context=context)


def blog_list(request):
    blogs = TypeArticle.objects.get(name='blog')
    posts = blogs.articles.all()
    return render(request, 'article/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    page = get_object_or_404(Article, slug=slug)
    comments = page.comments.filter(is_active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = page
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'page': page,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'article/blog_detail.html', context=context)
