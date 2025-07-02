from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.utils import db_get_all_category, db_get_finally_price, db_get_product, db_get_addons_by_product


def generate_category_menu(chat_id):
    """
    генерация inline-клавиатуры с категориями товаров.

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
    [builder.button(text=product.product_name, callback_data=f'product_view_{product.id}') for product in products]
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


def cart_actions_keyboard() -> InlineKeyboardMarkup:
    """кнопки оформления заказа и добавления/удаления товара в корзину"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📦 Оформить заказ', callback_data='confirm_order'),
        InlineKeyboardButton(text='➖ Убрать товар', callback_data='choose_to_remove'),
        InlineKeyboardButton(text='➕ Добавить товар', callback_data='choose_to_add')
    )
    builder.adjust(1, 2)

    return builder.as_markup()


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """кнопки настроек"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Сменить язык", callback_data="change_language")
    builder.button(text="🗑 Удалить аккаунт", callback_data="delete_account")
    builder.button(text="↩️ Назад", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """кнопки выбора языка"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.button(text="↩️ Назад", callback_data="settings_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_delete_confirm_keyboard() -> InlineKeyboardMarkup:
    """Подтверждение удаления аккаунта"""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, удалить", callback_data="confirm_delete")
    builder.button(text="❌ Отмена", callback_data="settings_menu")
    builder.adjust(1)
    return builder.as_markup()


def generate_addons_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Выбор добавок к товару"""
    addons = db_get_addons_by_product(product_id)
    builder = InlineKeyboardBuilder()
    for addon in addons:
        builder.button(
            text=f"{addon.name} (+{addon.price}BYN)",
            callback_data=f"addon_{addon.id}"
        )
    builder.button(text="✅ Без добавок", callback_data="no_addon")
    builder.adjust(1)
    return builder.as_markup()
