from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

from database.utils import db_get_user_cart, db_get_product_by_name, db_update_to_cart, db_add_or_update_item, \
    db_get_cart_items
from keyboards.inline import quantity_cart_controls
from bot_utils.message_utils import text_for_caption

router = Router()


@router.callback_query(F.data.regexp(r'action [+-]'))
async def change_product_quantity(callback: CallbackQuery, bot: Bot):
    """изменение количества товаров в корзине"""
    chat_id = callback.from_user.id
    message_id = callback.message.message_id
    action = callback.data.split()[-1]

    product_name = callback.message.caption.split('\n')[0]
    product = db_get_product_by_name(product_name)
    cart = db_get_user_cart(chat_id)

    if not product or not cart:
        await callback.answer("Ошибка: товар или корзина не найдены", show_alert=True)
        return

    increment = 1 if action == '+' else -1

    result = db_add_or_update_item(cart_id=cart.id, product_name=product.product_name, product_price=product.price,
                                   increment=increment)

    if result["status"] == "error":
        await callback.answer("Ошибка при изменении количества", show_alert=True)
        return

    addons_total = 0
    cart_items = db_get_cart_items(chat_id)
    for item in cart_items:
        if item["product_name"] == product.product_name:
            addons_total = item["addons_total"]
            break

    caption = text_for_caption(
        name=product.product_name,
        description=product.description,
        base_price=float(product.price) * result["product_quantity"],
        addon_price=float(addons_total)
    )

    try:
        await bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(
                media=FSInputFile(path=product.image),
                caption=caption,
                parse_mode='HTML'
            ),
            reply_markup=quantity_cart_controls(result["product_quantity"])
        )
    except TelegramBadRequest:
        pass
