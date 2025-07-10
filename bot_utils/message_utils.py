from database.utils import db_get_final_cart_items, db_get_cart_addons_by_cart_id


def text_for_caption(name, description, base_price, addon_price=0.0):
    """формирует текст описания товара с учетом добавок"""
    total_price = float(base_price) + float(addon_price)
    text = (
        f"<b>{name}</b>\n\n"
        f"<b>Описание:</b> {description}\n\n"
        f"<b>Цена:</b> {total_price:.2f} BYN"
    )
    if addon_price:
        text += f"\n(включая добавки: +{addon_price:.2f} BYN)"
    return text



def counting_products_from_cart(chat_id, user_text):
    """считает продукты в finally_cart + добавки и формирует текст для менеджера"""
    products = db_get_final_cart_items(chat_id)
    if not products:
        return None

    text = f'<b>{user_text}</b>\n\n'
    total_products = total_price = count = 0

    for name, quantity, price, cart_id in products:
        count += 1
        total_products += quantity
        total_price += price

        text += f'<b>{count}. {name}</b>\n<b>Количество:</b> {quantity}\n<b>Стоимость:</b> {price} BYN\n'

        addons = db_get_cart_addons_by_cart_id(cart_id)

        if addons:
            text += f"<b>Добавки:</b>\n"
            for addon in addons:
                text += f" └ {addon.name} +{addon.price} BYN\n"
                total_price += addon.price

        text += "\n"

    text += (
        f"<b>Общее количество продуктов:</b> {total_products}\n"
        f"<b>Общая стоимость корзины:</b> {total_price} BYN"
    )

    return (count, text, total_price, cart_id)
