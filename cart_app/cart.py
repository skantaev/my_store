from decimal import Decimal

from my_store import settings
from my_store_app.models import Product


class ItemDoesNotExist(Exception):
    pass


class Cart(object):
    """
    Класс "корзина". Данные хранятся в виде словаря в сессиях, поэтому для работы с корзиной каждый раз создаются
    новые экземпляры, которые временно хранят данные корзины в форме словаря, где каждый ключ это pk товара из моделей,
    а его значение - словарь с данными по товару (количество, цена).
    """
    def __init__(self, request):
        """
        Конструктор объектов корзины. При создании экземпляру присваивается словарь с данными из сессий, если его нет
        в сессиях, то создается пустой.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self._cart = cart

    def __iter__(self):
        """
        Метод для итерации по корзине. По ключам из словаря self._cart получаем набор экзпляров товаров из базы данных,
        которые присваиваем к словарю. Возвращаем генератор значений из словаря.
        """
        products_ids = self._cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        for product in products:
            self._cart[str(product.pk)]['product'] = product

        for item in self._cart.values():
            yield item

    def __len__(self):
        """
        Метод для возращения длины корзины. Длина определяется как сумма количеств всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self._cart.values())

    def __save(self):
        """
        Внутренний метод для сохранения корзины в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self._cart
        self.session.modified = True

    def add(self, product, set_qnt, quantity=1):
        """
        Добавление товара в корзину или изменения его количества в ней.
        :param product: экземпляр товара
        :param set_qnt: булевая переменная, указывающая если нужно изменить количество, а не добавить товар.
        :param quantity: количество товара, которое нужно добавить или установить.
        """
        product_id = str(product.pk)

        if product_id not in self._cart:
            self._cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            if set_qnt:
                self._cart[product_id]['quantity'] = quantity
            else:
                self._cart[product_id]['quantity'] += quantity

        # Если значение больше чем на складе, ставим максимально возможное
        if self._cart[product_id]['quantity'] > product.stock:
            self._cart[product_id]['quantity'] = product.stock

        self.__save()

    def remove(self, product_id):
        """
        Удаление определенного вида товара из корзины. Если такого товара в корзине нет, то выбрасывается исключение
        "товар не существует".
        """
        if product_id in self._cart:
            del self._cart[product_id]
        else:
            raise ItemDoesNotExist

        self.__save()

    def get_total_price(self):
        """
        Метод возвращает полную сумму всех товаров в корзине.
        """
        total_price = 0

        for product_id in self._cart:
            total_price += self._cart[product_id]['quantity'] * Decimal(self._cart[product_id]['price'])

        return total_price

    def clear(self):
        """
        Метод для полной очистки корзины.
        """
        self._cart = {}
        self.__save()

