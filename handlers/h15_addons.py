from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import generate_addons_keyboard

router = Router()


@router.callback_query(F.data.startswith("product_"))
async def handle_product_selected(callback: CallbackQuery):
    """Показать доступные добавки для товара"""
    product_id = int(callback.data.split("_")[1])
    await callback.message.edit_text(
        "Выберите добавку для товара (или откажитесь):",
        reply_markup=generate_addons_keyboard(product_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("addon_"))
async def handle_addon_selected(callback: CallbackQuery):
    """добавить добавку к товару"""
    addon_id = int(callback.data.split("_")[1])

    await callback.message.edit_text(f"🧩 Добавка добавлена! ID: {addon_id}")
    await callback.answer()


@router.callback_query(F.data == "no_addon")
async def handle_no_addon(callback: CallbackQuery):
    """отказаться от добавок"""
    await callback.message.edit_text("Вы выбрали товар без добавок.")
    await callback.answer()
