from aiogram import Router, F
from aiogram.types import Message

from database.utils import  db_update_user, db_create_user_cart

router = Router()


@router.message(F.contact)
async def update_info_user(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number

    db_update_user(chat_id, phone)

    if db_create_user_cart(chat_id):
        await message.answer(text='Вы зарегистрированы')
