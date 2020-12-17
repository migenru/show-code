from django.db import models


class Accessbot(models.Model):
    id = models.IntegerField(verbose_name='Chat ID', primary_key=True, unique=True, db_index=True)
    username = models.CharField(verbose_name='Username telegram', max_length=30)
    first_name = models.CharField(verbose_name='Name in telegram', max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Chat for notificate'
        verbose_name_plural = 'Chats for notificate'
