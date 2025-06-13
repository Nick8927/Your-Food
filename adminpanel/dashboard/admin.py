from django.contrib import admin
from .models import Users, Categories, Products, Carts, FinallyCarts

admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(FinallyCarts)
