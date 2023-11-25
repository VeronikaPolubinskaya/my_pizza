from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderPayment, OrderDelivery
import random
import time
import random
import requests

@shared_task
def payment(order_id):
    """
    Задача для установления способа оплаты и подтверждения заказа через звонок.
    """
    order = Order.objects.get(id=order_id)

    if order.status == 'new':
        # pay_method = 'карта'
        #
        # OrderPayment.objects.create(
        #     order=order,
        #     payment_method=pay_method
        # )
        #
        # order.status = 'confirmed'
        # order.save()

        call_url = "https://zvanok.by/manager/cabapi_external/api/v1/phones/call/"

        phonenumber  = str(order.phone)
        print(phonenumber)

        response = requests.get(call_url, {
            'public_key': settings.ZVANOK_PUBLIC_KEY,
            'phone': phonenumber,
            'campaign_id': settings.ZVANOK_CAMPAIGN_ID,
        })
        response_call = response.json()
        print(response_call)

        if "call_id" in response_call:
            call_id = response_call["call_id"]

            # call_id = '231118153375347'
            time.sleep(100)

            status_url = "https://zvanok.by/manager/cabapi_external/api/v1/phones/call_by_id/"

            response = requests.get(status_url, {
                'public_key': settings.ZVANOK_PUBLIC_KEY,
                'call_id': call_id,
                'campaign_id': settings.ZVANOK_CAMPAIGN_ID,
            })
            response_data = response.json()
            print(response_data)

            if response_data:
                user_choice = response_data[0]['user_choice']
                if user_choice == "оплата наличными":
                    pay_method = 'наличные'

                    OrderPayment.objects.create(
                        order=order,
                        payment_method=pay_method
                    )

                    order.status = 'confirmed'
                    order.save()

                elif user_choice == "оплата картой":
                    pay_method = 'карта'

                    OrderPayment.objects.create(
                        order=order,
                        payment_method=pay_method
                    )

                    order.status = 'confirmed'
                    order.save()

                else:
                    print("отмена заказа")

            else:
                print('API не удалось подключить')
        else:
            print("не удалось дозвониться абоненту")
    if order.status == 'confirmed':
        order_created.apply_async(args=[order.id], queue='order_created', link=payment.s())
    else:
        pass
@shared_task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    if order.status == 'confirmed':
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

        order.status = 'mail_sent'
        order.save()

        if order.status == 'mail_sent':
            delivery.apply_async(args=[order.id], queue='delivery', link=order_created.s())

        return mail_sent



@shared_task
def delivery(order_id):
    """
    Задача для установления способа сервиса доставки заказа.
    """
    order = Order.objects.get(id=order_id)

    if order.status == 'mail_sent':
        service = random.choice(['Dominos.Delivery', 'Яндекс.Доставка', 'Ежа.by'])

        OrderDelivery.objects.create(
            order=order,
            delivery_service=service
        )

        order.status = 'ready'
        order.save()

    if order.status == 'ready':
        delivered.apply_async(args=[order.id], queue='delivered', link=delivery.s())


@shared_task
def delivered(order_id):
    """
    Задача для отправки уведомления о доставке заказа.
    """
    order = Order.objects.get(id=order_id)

    if order.status == 'ready':

        def get_promo_code(num_chars):
            code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            code = ''
            for i in range(0, num_chars):
                slice_start = random.randint(0, len(code_chars) - 1)
                code += code_chars[slice_start: slice_start + 1]
            return code

        order_delivery = order.orderdelivery_set.last()
        promocode= get_promo_code(5)

        subject = f'Заказ № {order.id}'
        message = f' {order.first_name},\n\n' \
                  f'Ваш заказ {order.id} отправлен службой доставки {order_delivery.delivery_service} .\n'\
                  f'Заказ будет доставлен в течение 30 минут.\n\n' \
                  f'Используйте промокод {promocode} при следующем заказе и получите скидку 20%.\n\n' \
                  f'Приятного аппетита!.\n' \

        mail_sent = send_mail(subject,
                              message,
                              'searchmp2@gmail.com',
                              [order.email])

        order.status = 'order_sent'
        order.save()

        return mail_sent
