import asyncio
from aiogram import Bot, Dispatcher

from scheduler import start_scheduler
from config import TOKEN
from handlers import (
    h1_on_startup, h2_get_contact, h3_order_handler,h4_categories_handler,
    h5_navigation_handlers, h6_product_detail,h7_cart_quantity, h8_add_to_cart,
    h9_open_cart_handler,h10_confirm_order, h11_cart_modify, h12_settings,
    h13_language, h14_delete_account, h15_addons)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h1_on_startup.router)
dp.include_router(h2_get_contact.router)
dp.include_router(h3_order_handler.router)
dp.include_router(h4_categories_handler.router)
dp.include_router(h5_navigation_handlers.router)
dp.include_router(h6_product_detail.router)
dp.include_router(h7_cart_quantity.router)
dp.include_router(h8_add_to_cart.router)
dp.include_router(h9_open_cart_handler.router)
dp.include_router(h10_confirm_order.router)
dp.include_router(h11_cart_modify.router)
dp.include_router(h12_settings.router)
dp.include_router(h13_language.router)
dp.include_router(h14_delete_account.router)
dp.include_router(h15_addons.router)



async def main():
    start_scheduler()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
