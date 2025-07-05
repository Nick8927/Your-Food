from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from database.utils import (
    db_get_product_by_id,
    db_get_user_cart,
    db_update_to_cart,
    db_get_addons_by_product
)
from keyboards.inline import quantity_cart_controls, generate_addons_option_buttons
from bot_utils.message_utils import text_for_caption
from keyboards.reply import phone_button

router = Router()


@router.callback_query(F.data.startswith("product_view_"))
async def show_product_detail(callback: CallbackQuery, bot: Bot):
    """Показывает детальную информацию о продукте если пользователь авторизован"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    product_id = int(callback.data.split('_')[-1])
    product = db_get_product_by_id(product_id)
    user_cart = db_get_user_cart(chat_id)

    if user_cart:
        db_update_to_cart(price=product.price, cart_id=user_cart.id)

        caption = text_for_caption(product.product_name, product.description, product.price)
        product_image = FSInputFile(path=product.image)

        await bot.send_photo(
            chat_id=chat_id,
            photo=product_image,
            caption=caption,
            parse_mode='HTML',
            reply_markup=quantity_cart_controls()
        )

        addons = db_get_addons_by_product(product.id)
        if addons:
            await bot.send_message(
                chat_id=chat_id,
                text='Желаете выбрать допы? 😊',
                reply_markup=generate_addons_option_buttons(product.id)
            )

    else:
        await ask_for_phone(chat_id, bot)

async def ask_for_phone(chat_id: int, bot: Bot) -> None:
    """Отправка запроса на номер телефона, если пользователь не авторизован"""
    await bot.send_message(
        chat_id=chat_id,
        text='Предоставьте Ваш номер телефона, чтобы сделать заказ',
        reply_markup=phone_button()
    )