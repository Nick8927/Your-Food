import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, get_contact, order_handler

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(get_contact.router)
dp.include_router(order_handler.router)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
