def generate_cart_text(cart_items: list) -> str:
    """Генерирует текст для сообщения с содержимым корзины"""
    if not cart_items:
        return "🛒 Ваша корзина пуста."

    text = "🛒 Содержимое корзины:\n\n"
    total = 0.0

    for item in cart_items:
        name = item.get("product_name", "Без названия")
        quantity = item.get("quantity", 0)
        final_price = item.get("final_price", 0)
        addon_price = item.get("addons_total", 0)

        try:
            subtotal = float(final_price) + float(addon_price)
        except (TypeError, ValueError):
            subtotal = 0.0

        total += subtotal
        text += f"{name} — {quantity} шт. — {subtotal:.2f} руб\n"

    text += f"\n💰 Итого: {total:.2f} руб"
    return text
