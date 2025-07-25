from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest

from database.utils import db_get_last_orders
from handlers.h2_get_contact import show_main_menu
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
    """Показывает последние 5 заказов с учетом добавок"""
    chat_id = message.chat.id
    orders = db_get_last_orders(chat_id)
    if not orders:
        await message.answer("У вас пока нет заказов.")
        return

    text = "🧾 Последние 5 заказов:\n\n"
    for item in orders:
        order = item["order"]
        addons = item["addons"]

        line_price = float(order.final_price)
        text += f"📦 {order.product_name} — {order.quantity} шт. — {line_price:.2f} BYN\n"

        if addons:
            addons_text = ", ".join([f"{a.name} (+{float(a.price):.2f} BYN)" for a in addons])
            text += f"     ➕ {addons_text}\n"

    await message.answer(text)


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
