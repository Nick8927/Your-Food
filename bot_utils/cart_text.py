def generate_cart_text(cart_items: list) -> str:
    """Генерация текста содержимого корзины"""
    if not cart_items:
        return "🛒 Ваша корзина пуста."

    text = "🛒 Содержимое корзины:\n\n"
    total = 0
    for item in cart_items:
        subtotal = float(item.final_price)
        total += subtotal
        text += f"{item.product_name} — {item.quantity} шт. — {subtotal:.2f} руб\n"
    text += f"\n💰 Итого: {total:.2f} руб"
    return text
