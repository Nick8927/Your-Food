from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from handlers.order_handler import handle_make_order

router = Router()


@router.message(F.text == '⬅ Назад')
async def return_to_category_menu(message: Message, bot: Bot):
    """
    Обработчик кнопки «⬅ Назад».
    Удаляет предыдущее сообщение и возвращает пользователя к выбору категории.
    """
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except TelegramBadRequest:
        pass

    await handle_make_order(message, bot)
