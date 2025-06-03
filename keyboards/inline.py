from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.utils import db_get_all_category, db_get_finally_price, db_get_product


def generate_category_menu(chat_id):
    """
    Генерация inline-клавиатуры с категориями товаров.

    :param chat_id: ID пользователя для получения суммы корзины.
    :return: InlineMarkup с кнопками категорий и корзинки.
    """
    categories = db_get_all_category()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'Корзина заказа ({total_price if total_price else 0} рублей)',
        callback_data='Корзина заказа'
    )

    [builder.button(text=category.category_name, callback_data=f'category_{category.id}')
     for category in categories]

    builder.adjust(1, 2)
    return builder.as_markup()


def show_product_by_category(category_id: int) -> InlineKeyboardMarkup:
    """кнопка для показа продуктов по категориям"""
    products = db_get_product(category_id)
    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name, callback_data=f'product_{product.id}') for product in products]
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="⬅ Назад", callback_data='return_to_category')
    )
    return builder.as_markup()

def quantity_cart_controls(quantity=1) -> InlineKeyboardMarkup:
    """кнопка для изменения количества товара в корзине"""
    builder = InlineKeyboardBuilder()
    builder.button(text='➖', callback_data='action -')
    builder.button(text=str(quantity), callback_data='quantity')
    builder.button(text='➕', callback_data='action +')
    builder.button(text='Положить в корзину  🛒', callback_data='положить в корзину')
    builder.adjust(3, 1)
    return builder.as_markup(resize_keyboard=True)
