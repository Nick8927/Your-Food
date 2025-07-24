from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.utils import db_get_cart_items
from keyboards.inline import  cart_actions_keyboard

router = Router()


@router.message(F.text == "🛒 Корзина")
async def handle_cart(message: Message):
    """Выводит содержимое корзины в ответ на нажатие reply-кнопки"""
    await show_cart(chat_id=message.chat.id, send_fn=message.answer)


# callback (inline-кнопка)
@router.callback_query(F.data == 'Корзина заказа')
async def open_cart(callback: CallbackQuery):
    """Выводит содержимое корзины в ответ на нажатие inline-кнопки"""
    await show_cart(chat_id=callback.from_user.id, send_fn=callback.message.answer)
    await callback.answer()


async def show_cart(chat_id: int, send_fn):
    cart_items = db_get_cart_items(chat_id)
    if not cart_items:
        await send_fn("🛒 Ваша корзина пуста.")
        return

    text = "🛒 Содержимое корзины:\n\n"
    total = 0
    for item in cart_items:
        addons_total = sum(addon["price"] for addon in item.get("addons", []))
        subtotal = float(item["final_price"]) + addons_total
        total += subtotal
        text += f"{item['product_name']} — {item['quantity']} шт. — {subtotal:.2f} руб\n"

    text += f"\n💰 Итого: {total:.2f} руб"

    await send_fn(text, reply_markup=cart_actions_keyboard())
