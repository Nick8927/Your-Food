from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from database.utils import db_register_user
from keybords.reply import phone_button

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
    else:
        await message.answer(text='Для связи нужен Ваш контактный номер', reply_markup=phone_button())


# @router.message(F.contact)
# async def update_info_user(message: Message):
#     chat_id = message.chat.id
#     phone = message.contact.phone_number
#
#     db_update_user(chat_id, phone)
#
#     if db_create_user_cart(chat_id):
#         await message.answer(text='Вы зарегистрированы')

