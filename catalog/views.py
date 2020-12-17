from django.shortcuts import render
from .models import Category, Product
from .logic_function import weather_temp
from analytics.models import BlackIP
from .forms import SearchForm, FavoriteForm
from extuser.models import ExtUser
from django.shortcuts import get_object_or_404
from sales_and_clients.forms import CartAddProductForm
from django.http import HttpResponse
from django.views.generic.list import ListView
from rest_framework import viewsets
from .serializers import ProductSerializer


def block_detail(func):
    def wrapper(request, *args, **kwargs):
        ip_addr = request.META['REMOTE_ADDR']
        black_ip = BlackIP.objects.filter(black_address=ip_addr)
        if len(black_ip):
            return render(request, '404.html')
        else:
            return_value = func(request, *args, **kwargs)
            return return_value

    return wrapper


def index(request):
    catalogs = Category.objects.all()
    catalogs_slider = Category.objects.all()[:3]
    context = {
        'temperature': weather_temp,
        'catalogs': catalogs,
        'catalogs_slider': catalogs_slider,
        'usd': 'n/a',
        'eur': 'n/a'
    }
    return render(request, 'index.html', context=context)


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'
    context_object_name = 'catalogs'


def products_all(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog_product_list.html', {'products': products})


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/catalog_current_list.html'
    context_object_name = 'products'
    ordering = 'title'

    def get_queryset(self):
        cat = Category.objects.get(slug=self.kwargs['slug'])
        self.select_ordering = self.request.GET.get('ordering')

        if not self.select_ordering:
            self.select_ordering = 'title'
        return Product.objects.filter(categoty=cat).order_by(self.select_ordering)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['cat'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


@block_detail
def product_card(request, slug):
    product = get_object_or_404(Product, slug=slug)
    favorite_product = Product.objects.get(slug=slug)

    if request.method == 'POST' and 'form' in request.POST:
        form = FavoriteForm(request.POST)

        if form.is_valid():
            user = ExtUser.objects.get(username=request.user.username)
            user.favorite_product.add(favorite_product)
            user.save()
            response = HttpResponse('Товар добавлен в избранное')
            return response
    else:
        form = FavoriteForm()

    if request.method == 'POST' and 'form_cart' in request.POST:
        form_cart = CartAddProductForm(request.POST)
        cart = Cart(request)

        if form_cart.is_valid():
            cd = form_cart.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return redirect('cart:cart_detail')

    else:
        form_cart = CartAddProductForm()

    return render(request, 'catalog/catalog_product_detail.html',
                  {'product': product, 'form': form, 'form_cart': form_cart, })


def get_product(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            get_title = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=get_title).exclude(quentity=0)
            return render(request, 'catalog/catalog_product_list.html', {'products': products})

    else:
        form = SearchForm()

    return render(request, 'catalog/search.html', {'form': form})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
