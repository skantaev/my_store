from django.forms import ModelForm
from my_store_app.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'pickup',
            'delivery_address',
            'comment',
        ]
