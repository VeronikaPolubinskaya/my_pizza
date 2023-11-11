from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
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
            payment.delay(order.id)

            order_created.delay(order.id)

            delivery.delay(order.id)

            delivered.delay(order.id)

            return render(request, 'created.html',
                          {'order': order})

    else:   #GET request
        form = OrderCreateForm
    return render(request, 'create.html',
                  {'cart': cart, 'form': form})


