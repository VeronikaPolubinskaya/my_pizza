from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm, OrderStatusForm
from cart.cart import Cart
from .tasks import order_created, payment, delivery, delivered

def order_create(request):
    cart = Cart(request)     #получаем текущую корзину из сесссии
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()   #создание нового экземпляра заказа
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            # запуск асинхроных задач
            payment.apply_async(args=[order.id], queue='payment')

            return render(request, 'created.html',
                          {'order': order})

    else:   #GET request
        form = OrderCreateForm
    return render(request, 'create.html',
                  {'cart': cart, 'form': form})


def order_status(request):

    if request.method == 'POST':
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']

            try:
                order = Order.objects.get(id=int(order_number))
                order_id = order.id


                order_status = order.status
                if order_status == 'new':
                    order_status = 'не подтвержден'
                elif order_status == 'confirmed':
                    order_status = 'подтвержден'
                elif order_status == 'mail_sent':
                    order_status = 'в процессе изготовления'
                elif order_status == 'ready':
                    order_status = 'готов'
                elif order_status == 'order_sent':
                    order_status = 'уже в пути'

            except Order.DoesNotExist:
                order_status = ' не найден'

            context = {
                'order_status': order_status,
                'order': order,
                'order_id': order_id,
            }
            return render(request, 'order_status_result.html', context)

    else:   #GET request
        form = OrderStatusForm
    return render(request, 'order_status_check.html',
                  {'form': form})
