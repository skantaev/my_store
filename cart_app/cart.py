from my_store import settings
from decimal import Decimal
from my_store_app.models import Product


class ItemDoesNotExist(Exception):
    pass


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self._cart = cart

    def __iter__(self):
        products_ids = self._cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        for product in products:
            self._cart[str(product.pk)]['product'] = product

        for item in self._cart.values():
            yield item

    def __len__(self):
        """
        Возвращает количество товаров в корзине как длину словаря cart.
        """
        return sum(item['quantity'] for item in self._cart.values())

    def __save(self):
        self.session[settings.CART_SESSION_ID] = self._cart
        self.session.modified = True

    def add(self, product, quantity=1):
        """
        Добавление товара в корзину.
        """
        product_id = str(product.pk)

        if product_id not in self._cart:
            self._cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            self._cart[product_id]['quantity'] += quantity

        self.__save()

    def remove(self, product_id):
        if product_id in self._cart:
            del self._cart[product_id]
        else:
            raise ItemDoesNotExist

        self.__save()

    def set_quantity(self, product_id, quantity):
        """
        Изменение количества выбранного товара в корзине.
        """
        if product_id in self._cart:
            self._cart[product_id]['quantity'] = quantity
        else:
            raise ItemDoesNotExist

        self.__save()

    def get_total_price(self):
        total_price = 0

        for product_id in self._cart:
            total_price += self._cart[product_id]['quantity'] * Decimal(self._cart[product_id]['price'])

        return total_price

    def clear(self):
        """
        Метод для очистки корзины.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
