# Generated by Django 2.2 on 2020-08-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200802_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to='blog/%Y/%m/$d', verbose_name='Cover post'),
        ),
    ]
