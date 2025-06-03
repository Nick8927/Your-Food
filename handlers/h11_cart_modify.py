from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import (
    db_get_product_for_delete,
    db_increase_product_quantity,
    db_decrease_product_quantity, db_get_cart_items
)
from keyboards.inline import cart_actions_keyboard
from keyboards.reply import back_to_main_menu

router = Router()


@router.callback_query(F.data == 'choose_to_add')
async def choose_product_to_add(callback: CallbackQuery):
    """обработчик кнопки "выбрать товар для добавления"""
    cart_products = db_get_product_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➕ {name}', callback_data=f'increase_{cart_id}')
    builder.button(text="⬅ Назад", callback_data="back_to_cart_review")
    builder.adjust(1)
    await callback.message.edit_text("Выберите товар для увеличения количества:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == 'choose_to_remove')
async def choose_product_to_remove(callback: CallbackQuery):
    """обработчик кнопки "выбрать товар для удаления"""
    cart_products = db_get_product_for_delete(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➖ {name}', callback_data=f'decrease_{cart_id}')
    builder.button(text="⬅ Назад", callback_data="back_to_cart_review")
    builder.adjust(1)
    await callback.message.edit_text("Выберите товар для уменьшения количества:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    """обработчик кнопки "увеличить количество"""
    cart_id = int(callback.data.split("_")[1])
    db_increase_product_quantity(cart_id)
    await callback.answer("Количество увеличено.")
    await choose_product_to_add(callback)


@router.callback_query(F.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    cart_id = int(callback.data.split("_")[1])
    db_decrease_product_quantity(cart_id)

    user_id = callback.from_user.id
    cart_items = db_get_cart_items(user_id)

    if not cart_items:
        await callback.message.edit_text(
            "🛒 Ваш заказ пуст, сделайте его заново.",
            reply_markup=back_to_main_menu()
        )
    else:

        text = "🛒 Содержимое корзины:\n\n"
        total = 0
        for item in cart_items:
            subtotal = float(item.final_price)
            total += subtotal
            text += f"{item.product_name} — {item.quantity} шт. — {subtotal:.2f} руб\n"
        text += f"\n💰 Итого: {total:.2f} руб"

        keyboard = cart_actions_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)

    await callback.answer()


@router.callback_query(F.data == "back_to_cart_review")
async def back_to_cart(callback: CallbackQuery):
    """обработчик кнопки "назад"""
    await callback.message.edit_text("Вот ваша корзина:", reply_markup=cart_actions_keyboard())
    await callback.answer()
