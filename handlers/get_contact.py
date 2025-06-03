from aiogram import Router, F
from aiogram.types import Message

from database.utils import  db_update_user, db_create_user_cart
from keyboards.reply import get_main_menu

router = Router()


@router.message(F.contact)
async def update_info_user(message: Message):
    """обновление данных юзера"""
    chat_id = message.chat.id
    phone = message.contact.phone_number

    db_update_user(chat_id, phone)

    if db_create_user_cart(chat_id):
        await message.answer(text='Вы зарегистрированы')

    await show_main_menu(message)


async def show_main_menu(message: Message):
    """показ основного меню"""
    await message.answer(
        text="Сделайте выбор",
        reply_markup=get_main_menu()
    )
