from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from my_store_auth_app.models import CustomUser

# Register your models here.


class CustomAdminModel(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'address', 'phone_number', 'orders', 'note')


admin.site.register(CustomUser, CustomAdminModel)
