from django.db import models
from django.utils.timezone import now


class Users(models.Model):
    name = models.CharField(max_length=70)
    telegram = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
        managed = False
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Categories(models.Model):
    category_name = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = 'categories'
        managed = False
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]


    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=25, unique=True)
    description = models.TextField()
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="products")

    class Meta:
        db_table = 'products'
        managed = False
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id"]


    def __str__(self):
        return self.product_name


class Carts(models.Model):
    status = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_products = models.IntegerField(default=0)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        db_table = 'carts'
        managed = False
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


    def __str__(self):
        return f"Cart #{self.id} (User: {self.user.name})"


class FinallyCarts(models.Model):
    product_name = models.CharField(max_length=50)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name="finally_items")

    class Meta:
        db_table = 'finally_carts'
        managed = False
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"


class Orders(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name='orders')
    product_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'orders'
        managed = False
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.product_name} x{self.quantity} — {self.final_price} руб"


class ProductAddons(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="addons")

    class Meta:
        db_table = 'product_addons'
        managed = False
        verbose_name = "Добавка к продукту"
        verbose_name_plural = "Добавки к продуктам"

    def __str__(self):
        return f"{self.name} (+{self.price} руб)"


class CartAddons(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name="addons")
    addon = models.ForeignKey(ProductAddons, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = 'cart_addons'
        managed = False
        verbose_name = "Добавка в корзине"
        verbose_name_plural = "Добавки в корзинах"

    def __str__(self):
        return f"{self.name} (+{self.price} руб)"


class OrderAddons(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="addons")
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    class Meta:
        db_table = 'order_addons'
        managed = False
        verbose_name = "Добавка в заказе"
        verbose_name_plural = "Добавки в заказах"

    def __str__(self):
        return f"{self.name} (+{self.price} руб)"
