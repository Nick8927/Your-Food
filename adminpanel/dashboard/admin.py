from django.contrib import admin
from .models import Users, Categories, Products, Carts, FinallyCarts


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram', 'phone')
    search_fields = ('name', 'telegram')


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    search_fields = ('category_name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('product_name',)


@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_products', 'total_price')


@admin.register(FinallyCarts)
class FinallyCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'final_price', 'quantity', 'cart')
    list_filter = ('cart',)
