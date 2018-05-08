from django import forms
from my_store_app.models import Review, Order


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'text',
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'pickup',
            'delivery_address',
            'comment',
        ]