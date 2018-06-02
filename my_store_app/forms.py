from django.forms import ModelForm, Textarea, TextInput
from my_store_app.models import Review, Order


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'text',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'rows': 5,
                                    'class': 'form-control',
                                    }),

        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'pickup',
            'delivery_address',
            'comment',
        ]
