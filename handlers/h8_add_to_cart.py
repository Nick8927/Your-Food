from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_user_cart, db_get_product_by_name, \
    db_get_addons_by_product, db_add_or_update_item
from handlers.h5_navigation_handlers import return_to_category_menu
from keyboards.inline import generate_addons_keyboard

router = Router()


@router.callback_query(F.data == 'положить в корзину')
async def add_to_cart(callback: CallbackQuery, bot: Bot):
    """добавляет товар в корзину"""
    chat_id = callback.from_user.id
    message = callback.message

    caption = message.caption
    if not caption:
        await bot.send_message(chat_id=chat_id, text="Ошибка: товар не определён.")
        return

    product_name = caption.split('\n')[0]
    cart = db_get_user_cart(chat_id)
    if not cart:
        await bot.send_message(chat_id=chat_id, text="Сначала нужно авторизоваться.")
        return

    product = db_get_product_by_name(product_name)
    result = db_add_or_update_item(cart_id=cart.id, product_name=product_name, product_price=product.price, increment=0)

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id + 1)
    except:
        pass
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except:
        pass

    addons = db_get_addons_by_product(product.id)
    if addons:
        await bot.send_message(chat_id=chat_id, text="Не желаете выбрать добавки? 😊", reply_markup=generate_addons_keyboard(product.id))

    if result["status"] == "ok":
        await bot.send_message(chat_id=chat_id, text="✅ Продукт добавлен в корзину")
    else:
        await bot.send_message(chat_id=chat_id, text="❌ Ошибка при добавлении")

    await return_to_category_menu(message, bot)
