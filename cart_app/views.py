from django.shortcuts import render, redirect
from cart_app.cart import Cart
from django.views.decorators.http import require_POST
from my_store_app.models import Product

# Create your views here.


@require_POST
def add_product(request, product_pk):
    cart = Cart(request)
    product = Product.objects.get(pk=product_pk)
    cart.add(product)


@require_POST
def remove_product(request, product_pk):
    cart = Cart(request)
    product = Product.objects.get(pk=product_pk)
    cart.remove(product)


def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart_app/cart.html', {'cart': cart})


@require_POST
def make_order(request):
    pass
