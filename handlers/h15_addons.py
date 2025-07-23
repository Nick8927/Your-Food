from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot_utils.message_utils import text_for_caption, show_cart_menu
from database.utils import (
    db_get_addon_by_id,
    db_add_addon_to_cart,
    db_get_user_cart,
    db_get_product_by_id,
    db_get_addons_total_price,
    db_remove_addon_from_cart,
    db_get_addons_by_product,
    db_remove_addons_for_product
)
from keyboards.inline import generate_addons_keyboard, generate_back_to_menu_keyboard

router = Router()


@router.callback_query(F.data.startswith("product_"))
async def handle_product_selected(callback: CallbackQuery, state: FSMContext):
    """Показываем доступные добавки для товара"""
    product_id = int(callback.data.split("_")[1])
    addons = db_get_addons_by_product(product_id)

    if addons:
        await state.update_data(cart_message_id=callback.message.message_id)

        try:
            await callback.message.delete()
        except:
            pass

        await callback.message.answer(
            "Выберите добавку для товара (или откажитесь):",
            reply_markup=generate_addons_keyboard(product_id)
        )
    else:
        await show_cart_menu(callback.message, callback.from_user.id)

    await callback.answer()


@router.callback_query(F.data.startswith("addon_"))
async def handle_addon_selected(callback: CallbackQuery, state: FSMContext):
    """Добавляем добавку и возвращаем корзину"""
    addon_id = int(callback.data.split("_")[1])

    product_id = int(callback.message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[1])

    success = db_add_addon_to_cart(callback.from_user.id, addon_id, product_id)
    if not success:
        await callback.answer("❌ Ошибка добавления")
        return

    try:
        await callback.message.delete()
    except:
        pass

    await show_cart_menu(callback.message, callback.from_user.id)

    await callback.answer("Добавка добавлена ✅")


@router.callback_query(F.data.startswith('no_addon_'))
async def handle_no_addon(callback: CallbackQuery):
    """Удалить все добавки у конкретного товара и вернуть корзину"""
    product_id = int(callback.data.split("_")[2])
    chat_id = callback.from_user.id
    cart = db_get_user_cart(chat_id)

    if not cart:
        await callback.answer("Корзина не найдена.")
        return

    db_remove_addons_for_product(cart.id, product_id)

    try:
        await callback.message.delete()
    except:
        pass

    await show_cart_menu(callback.message, chat_id)
    await callback.answer("✅ Без добавок")


@router.callback_query(F.data.startswith("remove_addon_"))
async def handle_remove_addon(callback: CallbackQuery, bot: Bot):
    """Удалить добавку и обновить caption"""
    addon_id = int(callback.data.split("_")[2])
    addon = db_get_addon_by_id(addon_id)

    success = db_remove_addon_from_cart(callback.from_user.id, addon_id)
    if not success:
        await callback.answer("❌ Не удалось удалить добавку")
        return

    cart = db_get_user_cart(callback.from_user.id)
    if not cart:
        await callback.answer("❌ Корзина не найдена")
        return

    product = db_get_product_by_id(addon.product_id)
    addons_total = db_get_addons_total_price(cart.id)

    new_caption = text_for_caption(
        name=product.product_name,
        description=product.description,
        base_price=float(product.price),
        addon_price=addons_total
    )

    try:
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id - 1,
            caption=new_caption,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"ОШИБКА: Не удалось обновить caption: {e}")

    await callback.message.edit_text(
        f"🗑 Добавка {addon.name} удалена!",
        reply_markup=generate_back_to_menu_keyboard()
    )
    await callback.answer()
