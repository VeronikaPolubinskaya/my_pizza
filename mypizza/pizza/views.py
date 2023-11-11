from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def pizza_list(request):
    pizza_category = Category.objects.get(name='Пицца')

    products = Product.objects.filter(category=pizza_category)

    cart_product_form = CartAddProductForm()
    return render(request, 'pizza_list.html', {
        'products': products,
        'cart_product_form': cart_product_form
    })

def sauce_list(request):

    pizza_category = Category.objects.get(name='Соусы')

    products = Product.objects.filter(category=pizza_category)

    cart_product_form = CartAddProductForm()
    return render(request, 'sauce_list.html', {
        'products': products,
        'cart_product_form': cart_product_form
    })