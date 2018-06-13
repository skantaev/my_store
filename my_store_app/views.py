from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

from .models import Category, Product, OrderItem
from .forms import OrderForm
from cart_app.cart import Cart
from .tasks import send_order_email

# Create your views here.


def view_category(request, category_id=None):
    if request.method == 'GET':
        categories = Category.objects.all()

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            product_list = Product.objects.filter(available=True, category=category)
        else:
            category = None
            product_list = Product.objects.filter(available=True)

        paginator = Paginator(product_list, 12)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {'categories': categories,
                   'products': products,
                   'category': category,
                   }
        return render(request, 'my_store_app/index.html', context)

    return HttpResponse(status=405)


def view_product(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        categories = Category.objects.all()

        context = {'categories': categories,
                   'product': product,
                   }

        return render(request, 'my_store_app/product.html', context)

    return HttpResponse(status=405)


@require_http_methods(['GET', 'POST'])
def make_order(request):
    form = OrderForm()

    # Создание заказа по методу POST
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            cart = Cart(request)

            # Защита от создания пустых заказов
            if not len(cart):
                return HttpResponse(status=400)

            for item in cart:
                product = item['product']
                purchase_price = item['price']
                quantity = item['quantity']

                OrderItem.objects.create(order=order, product=product, purchase_price=purchase_price, quantity=quantity)

            cart.clear()

            # Отправка сообщения асинхронно на электронную почту
            if form.cleaned_data['email']:
                send_order_email.delay(order.pk)

            return render(request, 'my_store_app/order_success.html', {'order': order})

    return render(request, 'my_store_app/order.html', {'form': form})
