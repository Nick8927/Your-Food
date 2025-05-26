from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.filters import Text

from database.utils import db_register_user
from handlers.get_contact import show_main_menu
from keyboards.reply import phone_button, start_keyboard

router = Router()


@router.message(CommandStart(deep_link="welcome"))
async def command_start_welcome(message: Message):
    """Обработка старта по ссылке с deep-link 'welcome'"""
    photo = FSInputFile("media/welcome.jpg")
    await message.answer_photo(
        photo=photo,
        caption=f"Добро пожаловать, <i>{message.from_user.full_name}</i>\nНажмите кнопку ниже, чтобы начать",
        parse_mode='HTML',
        reply_markup=start_keyboard()
    )


@router.message(CommandStart())
async def command_start(message: Message):
    """обработка команды start"""

    photo = FSInputFile("media/welcome.jpg")
    await message.answer_photo(
        photo=photo,
        caption=f"Добрый день, <i>{message.from_user.full_name}</i>\nНажмите кнопку ниже, чтобы начать",
        parse_mode='HTML',
        reply_markup=start_keyboard()
    )


@router.message(Text("🚀 Начать"))
async def handle_start_button(message: Message):
    """обработка нажатия кнопки 'Начать"""
    await handle_start(message)


async def handle_start(message: Message):
    """обработка нажатия кнопки 'Начать'"""
    await register_user(message)


async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if db_register_user(full_name, chat_id):
        await message.answer(text=f'Вы в мире вкуснях 🍰')
        await show_main_menu(message)
    else:
        await message.answer(
            text='Для связи нужен Ваш контактный номер',
            reply_markup=phone_button()
        )
