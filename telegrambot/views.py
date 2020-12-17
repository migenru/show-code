import json
import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
from article.models import Comment

from .models import Accessbot


TOKEN = r'#'
bot = telebot.TeleBot(TOKEN)
URL = f'https://api.telegram.org/bot{TOKEN}'


@csrf_exempt
@bot.message_handler(content_types=["text"])
def webhook(request):
    body = request.body
    body_json = json.loads(body.decode('utf-8'))

    text = body_json['message']['text']
    chat_id = body_json['message']['chat']['id']
    data = {'chat_id': chat_id, 'text': text}
    bot.send_message(chat_id, text)
    return HttpResponse('<h1>Start</h1>')


@bot.message_handler(content_types=["text"])
@receiver(post_save, sender=Comment)
def new_comment(sender, **kwargs):
    chats = Accessbot.objects.all()
    text = f"Новый комментарий к статье: {kwargs['instance'].article.title}\n" \
        f"от {kwargs['instance'].name}.\n" \
        f"Он написал: {kwargs['instance'].content}"
    for chat in chats:
        text_with_name = f'{chat.first_name} ' + text
        bot.send_message(chat.id, text_with_name)
