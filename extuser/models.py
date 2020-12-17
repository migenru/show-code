from django.db import models
from catalog.models import Product
from django.contrib.auth.models import AbstractUser


class ExtUser(AbstractUser):
    USER_TYPE = [
        ('S', 'Сотрудник'),
        ('C', 'Клиент'),
    ]
    second_name = models.CharField(verbose_name='Отчество', max_length=200, blank=True)
    user_type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE, max_length=1, default='C')
    phone = models.CharField(verbose_name='Телефон', max_length=15, unique=True, blank=True)
    avatar = models.ImageField(verbose_name='Фото профиля', upload_to='user', blank=True)
    favorite_product = models.ManyToManyField(Product, verbose_name='Избранный товар', blank=True, related_name='user')
    date_register = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
