from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from database.utils import db_get_product_by_id, db_get_user_cart, db_update_to_cart
from keyboards.inline import quantity_cart_controls
from keyboards.reply import phone_button, back_arrow_button
from bot_utils.message_utils import text_for_caption

router = Router()


@router.callback_query(F.data.contains('product_'))
async def show_product_detail(callback: CallbackQuery,bot: Bot):
    """показывает детальную информацию о продукте и добавляет его в корзину, если пользователь авторизован"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    product_id = int(callback.data.split('_')[-1])
    product = db_get_product_by_id(product_id)

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    user_cart = db_get_user_cart(chat_id)
    if user_cart:
        db_update_to_cart(price=product.price, cart_id=user_cart.id)
        text = text_for_caption(product.product_name, product.description, product.price)

        await bot.send_message(
            chat_id=chat_id,
            text='Вы можете выбрать количество товара и добавить его в корзину',
            reply_markup=back_arrow_button()
        )
        await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(path=product.image),
            caption=text,
            parse_mode='HTML',
            reply_markup=quantity_cart_controls()
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text='Предоставьте Ваш номер телефона, чтобы сделать заказ',
            reply_markup=phone_button()
        )


