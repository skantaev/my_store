from django.shortcuts import render
from my_store_app.models import Category, Product
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
    pass