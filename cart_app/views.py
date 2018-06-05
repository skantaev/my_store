from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from cart_app.cart import Cart, ItemDoesNotExist
from my_store_app.models import Product

# Create your views here.


def add_product(request):
    product_id = request.GET.get('id', None)
    quantity = request.GET.get('quantity', None)

    product = get_object_or_404(Product, pk=product_id)
    if not product.available:
        return HttpResponse(status=403)

    cart = Cart(request)

    if quantity:
        try:
            quantity = int(quantity)
        # Если quantity не числовое
        except ValueError:
            return HttpResponse(status=400)

        cart.add(product, quantity)
    else:
        cart.add(product)

    return HttpResponse(status=200)


def set_quantity(request):
    product_id = request.GET.get('id', None)
    quantity = request.GET.get('quantity', None)
    cart = Cart(request)

    try:
        cart.set_quantity(product_id=product_id, quantity=int(quantity))
    except ItemDoesNotExist:
        return HttpResponse(status=404)
    except ValueError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


def clear(request):
    cart = Cart(request)
    cart.clear()

    return HttpResponse(status=200)


def remove_product(request):
    product_id = request.GET.get('id', None)
    cart = Cart(request)
    try:
        cart.remove(product_id)
    except ItemDoesNotExist:
        return HttpResponse(status=404)

    return HttpResponse(status=200)


def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart_app/cart.html', {'cart': cart})
