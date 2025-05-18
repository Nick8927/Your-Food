from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def phone_button():
    """кнопка для отправки телефонного номера"""
    builder = ReplyKeyboardBuilder()
    builder.button(text='Отправьте Ваш номер телефона ☎', request_contact=True)
    return builder.as_markup(resize_keyboard=True)


def get_main_menu():
    """формирование кнопок меню"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="✅ Сделать заказ")
    builder.button(text="📒 История")
    builder.button(text="🛒 Корзина")
    builder.button(text="⚙ Настройки")
    builder.adjust(1, 3)
    return builder.as_markup(resize_keyboard=True)


def back_to_main_menu():
    """кнопка возврата в главное меню"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Главное меню")
    return builder.as_markup(resize_keyboard=True)


def back_arrow_button():
    """кнопка назад"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="⬅ Назад")
    return builder.as_markup(resize_keyboard=True)
