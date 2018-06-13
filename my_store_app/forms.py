from django.forms import ModelForm, TextInput, Textarea, CheckboxInput

from .models import Order

TEXT_INPUT = TextInput(attrs={'class': 'form-control'})


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'phone_number',
            'email',
            'pickup',
            'delivery_address',
            'comment',
        ]
        widgets = {
            'customer_name': TEXT_INPUT,
            'phone_number': TEXT_INPUT,
            'email': TEXT_INPUT,
            'pickup': CheckboxInput(attrs={'class': 'form-inline'}),
            'delivery_address': TEXT_INPUT,
            'comment': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
        labels = {
            'customer_name': 'Имя*',
            'phone_number': 'Номер телефона*',
            'pickup': 'Самовывоз',
            'delivery_address': 'Полный адрес',
            'comment': 'Комментарий',
        }
