from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from database.utils import db_register_user
from handlers.get_contact import show_main_menu
from keyboards.reply import phone_button

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    """обработка команды start"""
    await message.answer(
        f"Добрый день, <i>{message.from_user.full_name}</i>\nДобро пожаловать",
        parse_mode='HTML'
    )
    await register_user(message)

async def register_user(message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if db_register_user(full_name, chat_id):
        await message.answer(text=f'Вы в мире вкуснях 🍰')
        await show_main_menu(message)
    else:
        await message.answer(text='Для связи нужен Ваш контактный номер', reply_markup=phone_button())



