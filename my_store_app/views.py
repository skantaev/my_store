from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from my_store_app.models import Category, Product, Review
from my_store_app.forms import ReviewForm

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


@require_http_methods(['GET', 'POST'])
def view_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    review_form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = request.user

            if not user.is_authenticated:
                user = get_user_model().objects.get_or_create(username='Аноним')[0]

            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            review = Review(user=user, product=product, title=title, text=text)
            review.save()

    categories = Category.objects.all()
    reviews = Review.objects.filter(product=product)

    if request.method == 'GET':
        paginator = Paginator(reviews, 10)
        page = request.GET.get('page')
        reviews = paginator.get_page(page)

    context = {'categories': categories,
               'product': product,
               'reviews': reviews,
               'form': review_form,
               }

    return render(request, 'my_store_app/product.html', context)
