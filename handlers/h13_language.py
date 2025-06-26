from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.utils import db_update_user_language
from keyboards.inline import get_language_keyboard, get_settings_keyboard

router = Router()


@router.callback_query(F.data == "change_language")
async def handle_change_language(callback: CallbackQuery):
    """обработка кнопки '🌐 Сменить язык'"""
    await callback.message.edit_text("Выберите язык:", reply_markup=get_language_keyboard())


@router.callback_query(F.data.startswith("lang_"))
async def handle_set_language(callback: CallbackQuery):
    """функция смены языка и сохранения в БД"""
    new_lang = callback.data.split("_")[1]
    telegram_id = callback.from_user.id

    db_update_user_language(telegram_id, new_lang)

    text = "✅ Язык установлен: Русский" if new_lang == "ru" else "✅ Language set: English"
    await callback.message.edit_text(text, reply_markup=get_settings_keyboard())
