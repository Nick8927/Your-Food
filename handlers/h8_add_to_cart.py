from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_user_cart, db_upsert_final_cart_item
from handlers.h5_navigation_handlers import return_to_category_menu

router = Router()


@router.callback_query(F.data == 'положить в корзину')
async def add_to_cart(callback: CallbackQuery, bot: Bot):
    """Обработчик кнопки 'Положить в корзину'"""
    chat_id = callback.from_user.id
    message = callback.message

    caption = message.caption
    if not caption:
        await bot.send_message(chat_id=chat_id, text="Ошибка: товар не определён.")
        return

    product_name = caption.split('\n')[0]
    cart = db_get_user_cart(chat_id)

    if not cart:
        await bot.send_message(chat_id=chat_id, text="Пожалуйста, сначала выберите товар.")
        return

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id + 1)
    except Exception as e:
        print(f"[!] Не удалось удалить сообщение с добавками: {e}")
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except Exception as e:
        print(f"[!] Не удалось удалить сообщение с продуктом: {e}")

    result = db_upsert_final_cart_item(
        cart_id=cart.id,
        product_name=product_name,
        total_products=cart.total_products,
        total_price=cart.total_price
    )

    match result:
        case 'inserted':
            await bot.send_message(chat_id=chat_id, text='Продукт добавлен ✅')
        case 'updated':
            await bot.send_message(chat_id=chat_id, text='Количество изменено 💫')
        case 'error':
            await bot.send_message(chat_id=chat_id, text='Произошла ошибка при добавлении ❌')

    await return_to_category_menu(message, bot)
