from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile

from database.utils import (
    db_get_product_by_id,
    db_get_user_cart,
    db_get_cart_items, db_get_all_category, db_add_or_update_item
)
from keyboards.inline import quantity_cart_controls, generate_category_menu
from keyboards.reply import phone_button
from bot_utils.message_utils import text_for_caption

router = Router()


@router.callback_query(F.data.startswith("product_view_"))
async def show_product_detail(callback: CallbackQuery, bot: Bot):
    """Показывает детальную информацию о продукте, если пользователь авторизован"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    product_id = int(callback.data.split('_')[-1])
    product = db_get_product_by_id(product_id)
    user_cart = db_get_user_cart(chat_id)

    if user_cart:
        db_add_or_update_item(
            cart_id=user_cart.id,
            product_id=product.id,
            product_name=product.product_name,
            product_price=product.price,
            increment=+1
        )

        cart_items = db_get_cart_items(chat_id)
        addons_total = 0
        for item in cart_items:
            if item["product_id"] == product.id:
                addons_total = sum(a["price"] for a in item["addons"])
                break

        caption = text_for_caption(
            name=product.product_name,
            description=product.description,
            base_price=float(product.price),
            addon_price=float(addons_total)
        )

        product_image = FSInputFile(path=product.image)

        await bot.send_photo(
            chat_id=chat_id,
            photo=product_image,
            caption=caption,
            parse_mode='HTML',
            reply_markup=quantity_cart_controls()
        )

    else:
        await ask_for_phone(chat_id, bot)


async def ask_for_phone(chat_id, bot: Bot):
    """Запрос номера телефона, если пользователь не авторизован"""
    await bot.send_message(
        chat_id=chat_id,
        text='Предоставьте Ваш номер телефона, чтобы сделать заказ',
        reply_markup=phone_button()
    )


@router.callback_query(F.data == "from_detail_to_category")
async def handle_back_to_category(callback: CallbackQuery, bot: Bot):
    """возврат от детального просмотра продукта к списку всех категорий"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f" Не удалось удалить сообщение: {e}")

    categories = db_get_all_category()

    if not categories:
        await bot.send_message(chat_id=chat_id, text=" Категории не найдены.")
        return

    keyboard = generate_category_menu(chat_id)
    await bot.send_message(
        chat_id=chat_id,
        text="Выберите категорию:",
        reply_markup=keyboard
    )

    await callback.answer()