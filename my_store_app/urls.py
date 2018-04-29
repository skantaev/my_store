from django.urls import path
from .views import view_category, view_product

app_name = 'my_store_app'

urlpatterns = [
    path('category/<int:category_id>', view_category, name='category'),
    path('product/<int:product_id>', view_product, name='product'),
]

