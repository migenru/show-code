from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from catalog.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    return render(request, 'sales_and_clients/cart_detail.html', {'cart': cart})
