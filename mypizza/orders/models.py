from django.db import models
from pizza.models import Product

class Order(models.Model):
    STATUSES = [('new', 'Новый'), ('confirmed', 'Подтвержден'), ('ready', 'Готов'), ('mail_sent', 'Отправлено уведомление'), ('order_sent', 'Заказ отправлен') ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=32, choices=STATUSES, default='new')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'Оплата заказа {self.order.id} от {self.payment_date}'


class OrderDelivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_service = models.CharField(max_length=50)
    delivery_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return f'Служба доставки заказа {self.order.id} от {self.delivery_date}'
