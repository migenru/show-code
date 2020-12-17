from collections import Counter
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify

from .forms import LoginForm, UserForm
from article.models import Article
from analytics.models import CountForIP
from catalog.models import Product
from extuser.models import ExtUser


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'backoffice/dashboard.html')
            else:
                return HttpResponse('Пользователь не найден')

        else:
            return HttpResponse('Неправильные логин или пароль')

    else:
        form = LoginForm()

    return render(request, 'backoffice/login.html', {'form': form})


def main(request):
    return render(request, 'backoffice/dashboard.html')


def favorite_list(request):
    username = request.user.username
    user = ExtUser.objects.get(username=username)
    products = user.favorite_product.all()
    return render(request, 'backoffice/favorite.html', {'products': products})


def profile_edit(request):
    username = request.user.username
    modeluser = ExtUser.objects.get(username=username)

    if request.method == 'POST':
        form = UserForm(request.POST, files=request.FILES, instance=modeluser)

        if form.is_valid():
            cd = form.cleaned_data

            if form.has_changed():
                modeluser = form.save(commit=False)
                error_msg = ''

                if 'new_password1' in form.changed_data:
                    if cd['new_password1'] != cd['new_password2']:
                        error_msg += '<li>Пароли не совпадают!!!</li>'
                    else:
                        modeluser.set_password(cd['new_password1'])
                        modeluser.save()

                if 'birthday' in form.changed_data:
                    now_date = date.today()
                    my_age = cd['birthday']
                    delta_date = now_date - my_age
                    age18 = 18 * 365
                    if delta_date.days < age18:
                        error_msg += '<li>Лицам младше 18 - запрещено!!!</li>'

                if error_msg:
                    return HttpResponse('<ol>' + error_msg + '</ol>')
                form.save()

                if 'avatar' in form.changed_data:
                    path_avatar = 'media/' + str(modeluser.avatar)
                    photo = Image.open(path_avatar)
                    drawing = ImageDraw.Draw(photo)
                    color = (169, 169, 169)
                    font = ImageFont.truetype("media/fonts/philosopher.ttf", 40)
                    pos = (0, 0)
                    text = modeluser.name
                    drawing.text(pos, text, fill=color, font=font)
                    photo.save(path_avatar)

            return render(request, 'backoffice/dashboard.html')

        else:
            context = {
                'form': form,
                'modeluser': modeluser
            }
            return render(request, 'backoffice/profile_edit.html', context)

    else:
        form = UserForm(instance=modeluser)
        context = {
            'form': form,
        }
        return render(request, 'backoffice/profile_edit.html', context)


class CreatePageView(CreateView):
    model = Article
    fields = ['image', 'title', 'content', 'tag', 'type', 'term']
    template_name = 'backoffice/create-form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePageView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(obj.title)
        obj.save()
        return HttpResponse('Страница создана')


def analitics(request):
    pages = CountForIP.objects.all().values_list('page_url', flat=True)
    populate_pages = Counter(pages).most_common(10)

    products = CountForIP.objects.filter(page_url__contains='product').values_list('page_url', flat=True)
    populate_products = Counter(products).most_common(10)
    return render(request, 'backoffice/analitics.html',
                  {'populate_pages': populate_pages, 'populate_products': populate_products})


def constructor_light(request):
    dictroom = {
        'bed': 0,
        'bed_count': 0,
        'bed_product': '',
        'kitchen': 0,
        'kitchen_count': 0,
        'kitchen_product': '',
        'living': 0,
        'living_count': 0,
        'living_product': '',
        'kids': 0,
        'kids_count': 0,
        'kids_product': '',
        'kids_description': '',
        'bath': 0,
        'bath_count': 0,
        'bath_product': '',
        'wc': 0,
        'wc_count': 0,
        'wc_product': '',
        'other': 0,
        'other_count': 0,
        'other_product': '',
    }
    data = ''
    product = ''
    if request.method == 'POST':
        home = request.POST['home']
        if home == 'house':
            data = 'Вам нужен уличный светильник. '
            product = Product.objects.get(slug='svetilnik-ulichnyi-es-altair-f-chernoe-zoloto-stolb-79')
        else:
            data = 'Вам не нужен уличный свет. '

        countroom = int(request.POST['countroom'])

        for i in range(countroom):
            typeid = 'typeroom_' + str(i + 1)
            squareid = 'square_' + str(i + 1)
            type_count = request.POST[typeid] + '_count'
            dict_key = request.POST[typeid]
            dict_value = request.POST[squareid]
            dictroom[dict_key] += int(dict_value)
            dictroom[type_count] += 1

        s = dictroom['bed'] + dictroom['kitchen'] + dictroom['kids'] \
            + dictroom['bath'] + dictroom['living'] + dictroom['wc'] \
            + dictroom['other']
        data += f'У вас {countroom} комнат. Общая площадь комнат: {s} кв.м'

        def description(typeroom, lumen):
            # функция по описанию светильников для каждой комнаты в зависимости от лм
            result = f'Вам нужна освещенность: {lumen * dictroom[typeroom]} лм. ' \
                f'Что равно {lumen * dictroom[typeroom] / 100} Вт светодиодных ламп. ' \
                f'Рекомендуем купить {int(lumen * dictroom[typeroom] / 100 // 5 + 1)} светодиодных ' \
                f'светильников мощностью по 5 Вт. '
            return result

        if dictroom['kids']:
            dictroom['kids_description'] = description('kids', 200) + f'Также не забудьте купить ночник в ' \
                                                                      f'количестве {dictroom["kids_count"]} шт.'
            dictroom['kids_product'] = Product.objects.filter(Q(title__icontains='Ночник') | Q(title__icontains="Потолочный"))[:3]

        if dictroom['bed']:
            dictroom['bed_description'] = description('bed', 150) + f'Также вам нужно бра в количестве {dictroom["bed_count"]*2} шт.'
            dictroom['bed_product'] = Product.objects.filter(title__icontains='Бра')[:3]

        if dictroom['kitchen']:
            dictroom['kitchen_description'] = description('kitchen', 150)
            dictroom['kitchen_product'] = Product.objects.filter(title__icontains='Спот')[:3]

        if dictroom['living']:
            dictroom['living_description'] = description('living', 150)
            dictroom['living_product'] = Product.objects.filter(Q(title__icontains='Люстра') | Q(title__icontains="Потолочный"))[:3]

        dictroom['living_description'] = description('living', 150)
        dictroom['bath_description'] = description('bath', 100)
        dictroom['wc_description'] = description('wc', 50)
        dictroom['other_description'] = description('other', 75)

        return render(request, 'backoffice/constructor.html', {'data': data, 'product': product, 'dictroom': dictroom})

    else:
        return render(request, 'backoffice/constructor.html', {'data': data, 'product': product, 'dictroom': dictroom})

    return render(request, 'backoffice/constructor.html', {'data': data, 'product': product, 'dictroom': dictroom})
