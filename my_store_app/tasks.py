from celery import shared_task
from django.core.mail import send_mail, mail_managers

from .models import Order, OrderItem


@shared_task
def send_order_email(order_id):
    """
    После создания заказа эта функция отправляет email покупателю и менеджеру с информацией о заказе.
    """
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    order_list = []
    for item in order_items:
        order_list.append('{} ({} шт.) – {} руб.'.format(item.product.name, item.quantity, item.get_cost()))

    subject = 'Заказ номер №{}'.format(order.pk)
    message = "Уважаемый(ая) {}, Ваш заказ получен и поступил в обработку.\nВ ближайшее время по указанному номеру " \
              "телефона ({}) с Вами свяжется наш менеджер.\nВаш заказ:\n• ".format(order.customer_name, order.phone_number)\
              + '\n• '.join(order_list) + '\nОбщая сумма заказа: {} руб.'.format(order.get_full_cost())

    mail_managers('Новый заказ', 'Поступил новый заказ №{}.'.format(order.pk))
    send_mail(subject, message, 'delivery@mystore.com', [order.email])
