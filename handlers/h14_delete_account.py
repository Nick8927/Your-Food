from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.utils import db_delete_user_by_telegram_id
from keyboards.inline import get_delete_confirm_keyboard, get_settings_keyboard
from keyboards.reply import start_keyboard

router = Router()


@router.callback_query(F.data == "delete_account")
async def handle_delete_account(callback: CallbackQuery):
    """реакцию на кнопку о запросе на удаление аккаунта"""
    await callback.message.edit_text(
        "❗ Вы уверены, что хотите удалить аккаунт?\nДанные будут удалены безвозвратно.",
        reply_markup=get_delete_confirm_keyboard()
    )


@router.callback_query(F.data == "confirm_delete")
async def handle_confirm_delete(callback: CallbackQuery):
    """удаляет пользователя из БД"""
    telegram_id = callback.from_user.id
    success = db_delete_user_by_telegram_id(telegram_id)

    if success:
        await callback.message.edit_text("🗑 Ваш аккаунт удалён.\nВы можете начать заново.", reply_markup=start_keyboard())
    else:
        await callback.message.edit_text("⚠ Произошла ошибка при удалении аккаунта.", reply_markup=get_settings_keyboard())
