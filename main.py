from os import getenv
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keybords.inline import *
from keybords.reply import *
from database.utils import *

load_dotenv()
TOKEN = getenv('TOKEN')
dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message(CommandStart())
async def command_start(message):
    """обработка команды start"""
    await message.answer(f"Добрый день, <i>{message.from_user.full_name}</i>\nВы в гостях у вкуснях из под ножа 🍰",
    parse_mode='HTML')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
