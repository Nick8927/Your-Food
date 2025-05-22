import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import (
    on_startup, get_contact, order_handler,
    categories_handler, navigation_handlers, product_detail,
    cart_quantity, add_to_cart)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(on_startup.router)
dp.include_router(get_contact.router)
dp.include_router(order_handler.router)
dp.include_router(categories_handler.router)
dp.include_router(navigation_handlers.router)
dp.include_router(product_detail.router)
dp.include_router(cart_quantity.router)
dp.include_router(add_to_cart.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
