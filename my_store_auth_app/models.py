from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from my_store_app.models import Order


# Create your models here.


class CustomUser(AbstractUser):
    address = models.CharField(max_length=150, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^(?:(?:\+7)|8)\d{10}$', message="Номер должен быть в формате \"+7ХХХХХХХХХХ\" "
                                                                         "или \"8ХХХХХХХХХХ\"")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    orders = models.ForeignKey(Order, related_name='orders', null=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=140, blank=True)
