from celery import shared_task
from django.core.mail import send_mail
from .models import Order, OrderPayment, OrderDelivery
import random
import time

@shared_task
def payment(order_id):
    """
    Задача для установления способа оплаты и подтверждения заказа.
    """
    order = Order.objects.get(id=order_id)

    if order.status == 'new':
        pay_method = random.choice(['наличные', 'карта'])

        OrderPayment.objects.create(
            order=order,
            payment_method=pay_method
        )

        order.status = 'confirmed'
        time.sleep(5)
        order.save()



@shared_task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    payment = order.orderpayment_set.last()
    products = ""
    for item in order.items.all():
        products += f"{item.product.name} x {item.quantity}\n"

    subject = f'Заказ № {order.id}'
    message = f'Здравствуйте, {order.first_name},\n\n' \
              f'Ваш заказ подтвержден и будет готов в течение 30 мин. Благодарим за ожидание.\n'\
              f'Номер Вашего заказа: {order.id}.\n' \
              f'В заказ входит: {products}.\n' \
              f'Стоимость заказа: {order.get_total_cost()} p.\n' \
              f'Способ оплаты: {payment.payment_method}.'
    mail_sent = send_mail(subject,
                          message,
                          'searchmp2@gmail.com',
                          [order.email])
    return mail_sent


@shared_task
def delivery(order_id):
    """
    Задача для установления способа сервиса доставки заказа.
    """
    order = Order.objects.get(id=order_id)

    if order.status == 'confirmed':
        service = random.choice(['Dominos.Delivery', 'Яндекс.Доставка', 'Ежа.by'])

        OrderDelivery.objects.create(
            order=order,
            delivery_service=service
        )

        order.status = 'ready'
        time.sleep(5)
        order.save()


@shared_task
def delivered(order_id):
    """
    Задача для отправки уведомления о доставке заказа.
    """
    order = Order.objects.get(id=order_id)
    order_delivery = order.orderdelivery_set.last()

    subject = f'Заказ № {order.id}'
    message = f' {order.first_name},\n\n' \
              f'Ваш заказ {order.id} отправлен службой доставки {order_delivery.delivery_service} .\n'\
              f'Заказ будет доставлен в течение 30 минут.\n' \
              f'Приятного аппетита!.\n' \

    mail_sent = send_mail(subject,
                          message,
                          'searchmp2@gmail.com',
                          [order.email])
    return mail_sent
