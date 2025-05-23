from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest

from database.utils import db_get_last_orders
from handlers.get_contact import show_main_menu
from keyboards.reply import back_to_main_menu
from keyboards.inline import generate_category_menu
from aiogram.types import Message

router = Router()


@router.message(F.text == "✅ Сделать заказ")
async def handle_make_order(message: Message, bot):
    """
    Обработчик кнопки "Сделать заказ".
    Отправляет сообщение с выбором категории и возвращает кнопку для перехода в главное меню.
    """
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Приступаем к формированию заказа", reply_markup=back_to_main_menu())
    await message.answer(text="Выберите категорию", reply_markup=generate_category_menu(chat_id))


@router.message(F.text == "📒 История")
async def handle_order_history(message: Message):
    """
    Обработчик кнопки "История".
    Отправляет пользователю последние 5 заказов.
    """
    chat_id = message.chat.id
    orders = db_get_last_orders(chat_id)
    if not orders:
        await message.answer("У вас пока нет заказов.")
        return

    text = "🧾 Последние 5 заказов:\n\n"
    for order in orders:
        text += f"📦 {order.product_name} — {order.quantity} шт. — {order.final_price} руб\n"
    await message.answer(text)


# @router.message(F.text == "🛒 Корзина")
# async def handle_cart(message: Message):
#     """
#     Обработчик кнопки "Корзина".
#     Показывает содержимое текущей корзины.
#     """
#     chat_id = message.chat.id
#     cart_items = db_get_cart_items(chat_id)
#     if not cart_items:
#         await message.answer("🛒 Ваша корзина пуста.")
#         return
#
#     text = "🛒 Содержимое корзины:\n\n"
#     total = 0
#     for item in cart_items:
#         subtotal = float(item.final_price) * item.quantity
#         total += subtotal
#         text += f"{item.product_name} — {item.quantity} шт. — {subtotal:.2f} руб\n"
#
#     text += f"\n💰 Итого: {total:.2f} руб"
#     await message.answer(text)


@router.message(F.text == "Главное меню")
async def handle_main_menu(message: Message, bot: Bot):
    """
    Обработчик кнопки 'Главное меню'.
    Удаляет предыдущее сообщение и показывает главное меню.
    """
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except TelegramBadRequest:
        ...
    await show_main_menu(message)
