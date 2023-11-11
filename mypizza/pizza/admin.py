from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    # prepopulated_fields = {'slug': ('name',)}  # чтобы указать поля, в которых значение автоматически задается с использованием значения других полей
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_editable = ['price']    #для задания полей, которые могут быть отредактированы на странице отображения списка сайта администрирования
    # prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)
