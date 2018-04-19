CART_SESSION_ID = 'cart'


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product):
        if product.pk not in self.cart:
            self.cart[product.pk] = {'quantity': 1, 'price': product.price}
        else:
            self.cart[product.pk]['quantity'] += 1

        self.session.modified = True

    def remove(self, product):
        if product.pk in self.cart:
            if self.cart[product.pk]['quantity'] > 1:
                self.cart[product.pk]['quantity'] -= 1
            else:
                del self.cart[product.pk]

        self.session.modified = True
