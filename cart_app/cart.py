from django.core.exceptions import ValidationError
from my_store import settings
from decimal import Decimal
from django import template


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self._cart = cart

    def __iter__(self):
        return self._cart

    def __len__(self):
        """
        Возвращает количество товаров в корзине как длину словаря cart.
        """
        return len(self._cart)

    def __save(self):
        self.session[settings.CART_SESSION_ID] = self._cart
        self.session.modified = True

    def add(self, product):
        """
        Добавление товара в корзину. Ключу словаря cart в виде первичного ключа товара соответсвует число товаров в
        корзине (при добавлении оно автоматически равно 1).
        """
        if product.pk not in self._cart:
            self._cart[product.pk] = {'quantity': 1, 'product': product}
        else:
            raise ValidationError('Product is already in the cart!')

        self.__save()

    def remove(self, product):
        if product.pk in self._cart:
            del self._cart[product.pk]
        else:
            raise ValidationError('Product is not in the cart!')

        self.__save()

    def set_quantity(self, product, quantity):
        """
        Изменение количества выбранного товара в корзине.
        """
        if product.pk in self._cart:
            self._cart[product.pk]['quantity'] = quantity
        else:
            raise ValidationError('Product is not in the cart!')

        self.__save()

    def get_total_price(self):
        total_price = 0

        for product_pk in self._cart:
            total_price += self._cart[product_pk]['quantity'] * Decimal(self._cart[product_pk]['product'].price)

        return total_price


register = template.Library()


@register.simple_tag
def multiply(value, arg):
    return Decimal(value) * arg
