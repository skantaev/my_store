from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse

from cart_app.cart import Cart, ItemDoesNotExist
from my_store_app.models import Product

# Create your views here.


def add_product(request):
    product_id = request.GET.get('id', None)
    product = get_object_or_404(Product, pk=product_id)

    if not product.available:
        return HttpResponse(status=403)

    cart = Cart(request)
    cart.add(product)

    return HttpResponse(status=200)


def remove_product(request):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    cart.remove(product)


def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart_app/cart.html', {'cart': cart})


@require_POST
def make_order(request):
    pass
