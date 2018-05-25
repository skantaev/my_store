from decimal import Decimal
from django import template


def multiply(value, arg):
    """
    Собственный фильтр умножения для вычисления общей цены товаров одного наименования в шаблоне.
    """
    return Decimal(value) * arg


# Регистрация фильтра в бибилиотеке
register = template.Library()
register.filter('multiply', multiply)
