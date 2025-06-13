from django.db import models


class Users(models.Model):
    """класс для таблицы пользователей"""
    name = models.CharField(max_length=70)
    telegram = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    """класс для таблицы категорий"""
    category_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    """класс для таблицы продуктов"""
    product_name = models.CharField(max_length=25, unique=True)
    description = models.TextField()
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name


class Carts(models.Model):
    """класс для таблицы корзин"""
    status = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_products = models.IntegerField(default=0)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart #{self.id} (User: {self.user.name})"


class FinallyCarts(models.Model):
    """"класс для таблицы заказов"""
    product_name = models.CharField(max_length=50)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name="finally_items")

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"
