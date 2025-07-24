import os
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram import Bot
import logging
from dotenv import load_dotenv
from database.utils import db_get_order_info

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("TOKEN")
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID", "0"))


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/reminders.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)


async def remind_manager(order_id: int, manager_chat_id: int):
    bot = Bot(token=BOT_TOKEN)

    order_info = db_get_order_info(order_id)
    if not order_info:
        logger.error(f"Заказ с ID {order_id} не найден в БД для напоминания.")
        await bot.session.close()
        return

    text = (
        f"📌 Напоминание: заказ №{order_id} был оформлен ранее\n"
        f"Клиент: {order_info['username']}\n"
        f"Телефон: {order_info['phone']}\n"
        f"Сумма заказа: {order_info['total_price']:.2f} BYN"
    )

    await bot.send_message(manager_chat_id, text)
    await bot.session.close()
    logger.info(f"Напоминание менеджеру отправлено (order_id={order_id})")


def schedule_reminder(order_id: int):
    """Планируем напоминание через 1 минуту"""
    run_date = datetime.now() + timedelta(minutes=1)
    scheduler.add_job(
        remind_manager,
        "date",
        run_date=run_date,
        args=[order_id, MANAGER_CHAT_ID],
        id=f"reminder_{order_id}",
        replace_existing=True
    )
    logger.info(f"Задача для заказа {order_id} запланирована на {run_date}")


def start_scheduler():
    """Запускаем планировщик"""
    if not scheduler.running:
        scheduler.start()
        logger.info("Планировщик запущен")
