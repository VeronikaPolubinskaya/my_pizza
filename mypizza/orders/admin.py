from django.contrib import admin
from .models import Order, OrderItem, OrderPayment, OrderDelivery

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment


class OrderDeliveryInline(admin.TabularInline):
    model = OrderDelivery


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'phone', 'created_at', 'status']
    list_filter = ['created_at', 'created_at']
    inlines = [OrderItemInline, OrderPaymentInline, OrderDeliveryInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderPayment)
admin.site.register(OrderDelivery)