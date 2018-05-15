from django.shortcuts import render, get_object_or_404
from my_store_app.models import Category, Product, Review
from django.http import HttpResponse

# Create your views here.


def index(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        context = {'categories': categories,
                   'products': products,
                   }
        return render(request, 'my_store_app/index.html', context)

    return HttpResponse(status=405)


def view_category(request, category_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        category = get_object_or_404(Category, pk=category_id)
        products = Product.objects.filter(available=True, category=category)
        context = {'categories': categories,
                   'products': products,
                   'category': category,
                   }
        return render(request, 'my_store_app/index.html', context)

    return HttpResponse(status=405)


def view_product(request, product_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        product = get_object_or_404(Product, pk=product_id)
        reviews = Review.objects.filter(visible=True, product=product)
        context = {'categories': categories,
                   'product': product,
                   'reviews': reviews,
                   }
        return render(request, 'my_store_app/product.html', context)

    return HttpResponse(status=405)
