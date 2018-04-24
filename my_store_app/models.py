from django.db import models
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=3000, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    goods = models.ManyToManyField(Product, blank=True, related_name='goods')

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
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
