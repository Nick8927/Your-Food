from database.utils import db_get_cart_items
from keyboards.inline import cart_actions_keyboard
from aiogram.types import Message


def text_for_caption(name, description, base_price, addon_price=0.0):
    """формирует текст описания товара с учетом добавок"""
    total_price = float(base_price) + float(addon_price)
    text = (
        f"<b>{name}</b>\n\n"
        f"<b>Описание:</b> {description}\n\n"
        f"<b>Цена:</b> {total_price:.2f} BYN"
    )
    if addon_price > 0:
        text += f" (включая добавки: +{addon_price:.2f} BYN)"
    return text


def counting_products_from_cart(chat_id, user_text):
    """ Считает продукты из корзины (с учетом добавок) и формирует текст для менеджера """
    items = db_get_cart_items(chat_id)
    if not items:
        return None

    text = f"<b>{user_text}</b>\n\n"
    total_products = total_price = count = 0
    cart_id = None

    for idx, item in enumerate(items, start=1):
        name = item["product_name"]
        qty = item["quantity"]
        base_price = float(item["final_price"])
        addons_total = sum(a["price"] for a in item["addons"])
        item_total = base_price + addons_total
        total_price += item_total
        total_products += qty
        count += 1
        cart_id = item["product_id"]

        text += f"<b>{idx}. {name}</b>\n"
        text += f"<b>Количество:</b> {qty}\n"
        text += f"<b>Стоимость:</b> {item_total:.2f} BYN\n"

        if item["addons"]:
            text += f"<b>Добавки:</b>\n"
            for addon in item["addons"]:
                text += f" └ {addon['name']} +{addon['price']:.2f} BYN\n"

        text += "\n"

    text += (
        f"<b>Общее количество продуктов:</b> {total_products}\n"
        f"<b>Общая стоимость корзины:</b> {total_price:.2f} BYN"
    )

    return count, text, total_price, cart_id


async def show_cart_menu(message: Message, chat_id: int):
    """Показывает корзину с учетом добавок и правильным пересчетом"""
    items = db_get_cart_items(chat_id)

    if not items:
        await message.answer("🛒 Ваша корзина пуста.")
        return

    text_lines = ["<b>🛍 Ваша корзина:</b>\n"]
    total_price = 0.0

    for item in items:
        name = item["product_name"]
        qty = item["quantity"]
        base_price = item["final_price"]
        addons_total = sum(a["price"] for a in item["addons"]) * qty
        item_total = base_price + addons_total
        total_price += item_total

        line_text = f"<b>{name}</b> ({qty} шт.) — {item_total:.2f} BYN"

        if item["addons"]:
            addons_text = ", ".join([f'{a["name"]} (+{a["price"]:.2f} BYN)' for a in item["addons"]])
            line_text += f"\n   ➕ Добавки: {addons_text}"

        text_lines.append(line_text)

    text_lines.append(f"\n<b>💰 Итого:</b> {total_price:.2f} BYN")

    await message.answer(
        "\n".join(text_lines),
        parse_mode="HTML",
        reply_markup=cart_actions_keyboard()
    )
