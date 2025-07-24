from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery

from scheduler import schedule_reminder
from action_logger import log_user_order
from bot_utils.message_utils import counting_products_from_cart
from config import MANAGER_CHAT_ID
from database.utils import db_clear_final_cart, db_get_user_phone, \
    db_remove_all_addons_from_cart, db_save_order_with_addons

router = Router()


@router.callback_query(F.data == "confirm_order")
async def handle_confirm_order(callback: CallbackQuery, bot: Bot):
    """обработчик кнопки '📦 Оформить заказ' """
    user = callback.from_user
    phone = db_get_user_phone(user.id)
    mention = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
    user_text = (
        f"Новый заказ от {mention}\n"
        f"<b>Телефон:</b> {phone}"
    )
    context = counting_products_from_cart(user.id, user_text)

    if not context:
        await callback.message.edit_text("❌ Невозможно оформить заказ: корзина пуста.")
        await callback.answer()
        return

    if not MANAGER_CHAT_ID:
        await callback.message.edit_text("❌ Ошибка: ID менеджера не задан.")
        await callback.answer()
        return

    count, text, total_price, cart_id = context

    await bot.send_message(MANAGER_CHAT_ID, text, parse_mode="HTML")

    orders_data, order_ids, total_price = db_save_order_with_addons(user.id)

    if order_ids:
        schedule_reminder(order_ids[0])

    db_clear_final_cart(callback.from_user.id)
    db_remove_all_addons_from_cart(callback.from_user.id)

    log_user_order(
        username=user.full_name,
        user_id=user.id,
        orders_data=orders_data,
        total_price=total_price
    )

    await callback.message.edit_text("✅ Ваш заказ отправлен менеджеру. Мы свяжемся с вами.\nЗаказ доступен в истории")
    await callback.answer("Заказ оформлен!")
