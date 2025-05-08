from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def phone_button():
    """кнопка для отправки телефонного номера"""
    builder = ReplyKeyboardBuilder()
    builder.button(text='Отправьте Ваш номер телефона ☎', request_contact=True)
    return builder.as_markup(resize_keyboard=True)