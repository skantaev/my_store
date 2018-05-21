from django import forms


class SetQuantityForm(forms.Form):
    quantity = forms.IntegerField(max_value=100, min_value=1)
