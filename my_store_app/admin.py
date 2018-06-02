from django.contrib import admin
from my_store_app.models import Category, Product, Order

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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'pickup', 'delivery_address', 'comment', 'received', 'date_created', 'date_received')
    list_filter = ('received', 'date_created', 'date_received')
    list_editable = ('received', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
