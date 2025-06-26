from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import get_settings_keyboard
from keyboards.reply import get_main_menu

router = Router()

@router.message(F.text == "⚙ Настройки")
async def handle_settings_menu(message: Message):
    """обработчик reply-кнопки '⚙ Настройки'"""
    await message.answer("🔧 Настройки", reply_markup=get_settings_keyboard())


@router.callback_query(F.data == "back_to_menu")
async def handle_back_to_main(callback: CallbackQuery):
    """обработчик inline-кнопки '↩️ Назад'"""
    await callback.message.delete()
    await callback.message.answer("📲 Главное меню  ⬇", reply_markup=get_main_menu())
