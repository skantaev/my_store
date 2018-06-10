from django.urls import path

from .views import view_cart, add_product, remove_product, clear

app_name = 'cart_app'

urlpatterns = [
    path('', view_cart, name='view'),
    path('add/', add_product, name='add'),
    path('remove/', remove_product, name='remove'),
    path('set/', add_product, name='set'),
    path('clear/', clear, name='clear'),
]
