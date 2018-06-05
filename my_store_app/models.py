from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import RegexValidator


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category', args=[self.pk])


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category = models.ManyToManyField(Category,
                                      blank=True,
                                      related_name='category',
                                      verbose_name='Категория',
                                      )
    description = models.TextField(max_length=3000, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='my_store_app/images/products/%Y/%m/%d/', null=True, blank=True,
                              verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name='В наличии')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product', args=[self.pk])


def get_sentinel_product():
    """
    Возвращает объект класса Product (или создает и возвращает, если его нет) для замещения удаленных объектов этого
    класса.
    """
    return Product.objects.get_or_create(name='deleted')[0]


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET(get_sentinel_product))
    quantity = models.PositiveIntegerField()


class OrderManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(received=True)


class OrderUnreceivedManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(received=False)


class Order(models.Model):
    items = models.ForeignKey(OrderItem, related_name='items', on_delete=models.PROTECT)

    customer_name = models.CharField(max_length=100)

    phone_regex = RegexValidator(regex=r'^(?:(?:\+7)|8)\d{10}$', message="Номер должен быть в формате \"+7ХХХХХХХХХХ\" "
                                                                         "или \"8ХХХХХХХХХХ\"")
    customer_phonenumber = models.CharField(validators=[phone_regex], max_length=15, blank=True)

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
