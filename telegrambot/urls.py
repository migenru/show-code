from django.urls import path
from .views import webhook


app_name = 'telebot'
urlpatterns = [
    path('', webhook, name="bot_start"),
]
