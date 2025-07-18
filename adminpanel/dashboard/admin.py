from django.contrib import admin
from .models import Users, Categories, Products, Orders


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


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'final_price', 'created_at')


