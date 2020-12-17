from django.contrib import admin

from .models import Accessbot


@admin.register(Accessbot)
class AccessbotAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name')
