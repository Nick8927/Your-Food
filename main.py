import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, get_contact

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(get_contact.router)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
