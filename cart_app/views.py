from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .cart import Cart, ItemDoesNotExist
from my_store_app.models import Product

# Create your views here.


def add_product(request):
    product_id = request.GET.get('id', None)
    quantity = request.GET.get('quantity', None)
    set_qnt = request.GET.get('set_qnt', False)

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

        cart.add(product=product, set_qnt=set_qnt, quantity=quantity)
    else:
        cart.add(product=product, set_qnt=set_qnt)

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
