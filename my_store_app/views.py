from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator

from my_store_app.models import Category, Product


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
