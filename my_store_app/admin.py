from django.contrib import admin

from .models import Category, Product, Order, OrderItem

# Register your models here.


class CategoryProductInline(admin.TabularInline):
    model = Product.category.through


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryProductInline,
    ]
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'available', 'date_created', 'date_updated')
    list_filter = ('available', 'date_created', 'date_updated')
    list_editable = ('price', 'stock', 'available')


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    list_display = ('id', 'pickup', 'delivery_address', 'comment', 'received', 'date_created')
    list_filter = ('received', 'date_created')
    list_editable = ('received', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
