from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from action_logger import log_user_deletion
from config import MANAGER_CHAT_ID
from database.utils import db_delete_user_by_telegram_id
from keyboards.inline import get_settings_keyboard, get_delete_confirm_keyboard
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
async def handle_confirm_delete(callback: CallbackQuery, bot: Bot):
    """удаляет пользователя, показывает старт и уведомляет админа"""
    telegram_id = callback.from_user.id
    full_name = callback.from_user.full_name
    success = db_delete_user_by_telegram_id(telegram_id)

    if success:
        log_user_deletion(username=full_name, user_id=telegram_id)

        try:
            await callback.message.delete()
        except Exception:
            pass

        await callback.message.answer(
            "🗑 Ваш аккаунт был успешно удалён.\n\n🚀 Нажмите кнопку ниже, чтобы начать заново.",
            reply_markup=start_keyboard()
        )

        await bot.send_message(
            MANAGER_CHAT_ID,
            f"❗ Пользователь <b>{full_name}</b> удалил аккаунт.\nTelegram ID: <code>{telegram_id}</code>",
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "⚠ Произошла ошибка при удалении аккаунта.",
            reply_markup=get_settings_keyboard()
        )
