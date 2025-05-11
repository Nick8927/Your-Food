from aiogram import Router, F
from keyboards.reply import back_to_main_menu
from keyboards.inline import generate_category_menu
from aiogram.types import Message

router = Router()


@router.message(F.text == "✅ Сделать заказ")
async def handle_make_order(message: Message, bot):
    """
    Обработчик кнопки "Сделать заказ".
    Отправляет сообщение с выбором категории и возвращает кнопку для перехода в главное меню.
    """
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Приступаем к формированию заказа", reply_markup=back_to_main_menu())
    await message.answer(text="Выберите категорию", reply_markup=generate_category_menu(chat_id))
