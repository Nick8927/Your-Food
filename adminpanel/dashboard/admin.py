from django.contrib import admin
from django.utils.safestring import mark_safe

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
    list_display = ('product_name', 'quantity', 'final_price')

    def custom_dashboard(context):
        return mark_safe(f"""
            <div class="card">
                <div class="card-header bg-primary text-white">Аналитика продаж</div>
                <div class="card-body">
                    <img src="/dashboard/sales-chart/" style="width:100%; height:auto;">
                </div>
            </div>
        """)

    admin.site.index_template = 'admin/custom_index.html'

