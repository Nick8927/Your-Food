from django.db import models


class Users(models.Model):
    """класс для таблицы пользователей"""
    name = models.CharField(max_length=70)
    telegram = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Categories(models.Model):
    """класс для таблицы категорий"""
    category_name = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = 'categories'
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category_name


class Products(models.Model):
    """класс для таблицы продуктов"""
    product_name = models.CharField(max_length=25, unique=True)
    description = models.TextField()
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="products")

    class Meta:
        db_table = 'products'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.product_name


class Carts(models.Model):
    """класс для таблицы корзин"""
    status = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_products = models.IntegerField(default=0)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="cart")

    class Meta:
        db_table = 'carts'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Cart #{self.id} (User: {self.user.name})"


class FinallyCarts(models.Model):
    """"класс для таблицы заказов"""
    product_name = models.CharField(max_length=50)
    final_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name="finally_items")

    class Meta:
        db_table = 'finally_carts'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"


class Orders(models.Model):
    """класс для таблицы orders"""
    cart = models.ForeignKey('Carts', on_delete=models.CASCADE, related_name='orders')
    product_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.quantity} — {self.final_price} руб"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "orders"
