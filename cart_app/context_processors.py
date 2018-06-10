from .cart import Cart


def cart(request):
    """
    Контекстный процессор для корзины товаров.
    """
    return {'cart': Cart(request)}
