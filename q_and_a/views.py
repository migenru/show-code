from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from extuser.models import ExtUser
from slugify import slugify


def index(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    return render(request, 'q_and_a/base_index.html', {'questions': questions, 'answers': answers, })


def only_staff(func):
    def wrapper(request, *args, **kwargs):
        user_type = request.user.user_type

        if user_type == 'S':
            return_value = func(request, *args, **kwargs)
            return return_value
        else:
            return render(request, '404.html')

    return wrapper

def only_customer(func):
    def wrapper(request, *args, **kwargs):
        user_type = request.user.user_type

        if user_type == 'C':
            return_value = func(request, *args, **kwargs)
            return return_value
        else:
            return render(request, '404.html')

    return wrapper

@only_customer
def create_question(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            question = Question()
            question.title = cd['title']
            question.content = cd['content']
            username = request.user.username
            user = ExtUser.objects.get(username=username)
            question.author = user
            question.slug = slugify(cd['title'])
            question.status = 'P'
            question.save()
            return HttpResponseRedirect('/q-and-a/create-question/')

    else:
        form = QuestionForm()

    type = 'вопрос'
    return render(request, 'backoffice/question_create.html', {'form': form, 'type': type})

@only_staff
def pre_create_answer(request):
    questions = Question.objects.filter(answer__isnull=True)
    return render(request, 'backoffice/question_choise.html', {'questions': questions})

@only_staff
def create_answer(request, id):
    question = Question.objects.get(id=id)
    username = request.user.username
    user = ExtUser.objects.get(username=username)

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            answer = Answer()
            answer.question = question
            answer.title = cd['title']
            answer.content = cd['content']
            answer.author = user
            answer.slug = slugify(cd['title'])
            answer.status = 'P'
            answer.save()
            return HttpResponseRedirect('/q-and-a/questions/')
    else:
        form = AnswerForm()

    type = 'ответ на вопрос: "' + question.title + '"'
    type_page = 'answer'
    return render(request, 'backoffice/question_create.html',
                  {'form': form, 'type': type, 'question': question, 'type_page': type_page})
