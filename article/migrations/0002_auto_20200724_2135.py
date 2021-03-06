# Generated by Django 2.2 on 2020-07-24 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, to='article.TagArticle', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='article',
            name='term',
            field=models.ManyToManyField(blank=True, to='article.TermArticle', verbose_name='Раздел записи'),
        ),
    ]
