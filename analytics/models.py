from django.db import models


class CountForIP(models.Model):
    page_url = models.CharField(verbose_name='Регистрация страницы', max_length=250)
    time = models.DateTimeField(verbose_name='Регистрация времени', auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        verbose_name = 'Cчетчик по IP'
        verbose_name_plural = 'Cчетчики по IP'
        ordering = ['-time']

    def __str__(self):
        return self.ip_address


class BlackIP(models.Model):
    black_address = models.GenericIPAddressField()
    time = models.DateTimeField(verbose_name='Добавлен в blacklist', auto_now_add=True)

    class Meta:
        verbose_name = 'Blacklist по IP'
        verbose_name_plural = 'Blacklists по IP'

    def __str__(self):
        return self.black_address
