from django.db import models
from django.utils import timezone
from django.conf import settings
from my_store_auth_app import models as auth_models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category,
                                      blank=True,
                                      null=True,
                                      related_name='category',
                                      verbose_name='Категория',
                                      )
    description = models.TextField(max_length=3000, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    number_of_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(auth_models.get_user_model))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.CharField(max_length=3000, verbose_name='Текст')
    visible = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


def get_sentinel_product():
    return Product.objects.get_or_create(name='deleted')


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.S)
    quantity = models.PositiveIntegerField()


class OrderManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(received=True)


class OrderUnreceivedManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(received=False)


class Order(models.Model):
    items = models.ForeignKey(OrderItem, related_name='items', on_delete=models.PROTECT)
    pickup = models.BooleanField()
    delivery_address = models.CharField(max_length=150, null=True)
    comment = models.CharField(max_length=500, blank=True)
    received = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(null=True)

    objects = models.Manager()
    delivered_manager = OrderManager()
    undelivered_manager = OrderUnreceivedManager()

    def mark_received(self, commit=True):
        self.received = True
        self.date_received = timezone.now()
        if commit:
            self.save()

    def __str__(self):
        return 'Order №[%s]' % self.pk
