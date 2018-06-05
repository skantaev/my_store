from django.forms import TextInput, ModelForm, PasswordInput

from my_store_auth_app.models import CustomUser


class RegistrationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'address',
            'phone_number',
        ]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'e'

        }
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password': 'Пароль',

        }
        help_texts = {
            'username': None,
        }
