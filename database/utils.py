from typing import Iterable
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select, DECIMAL
from sqlalchemy.sql.functions import sum
from sqlalchemy.exc import IntegrityError
from database.models import Users, Categories, Products, Carts, FinallyCarts
from database.base import engine
from sqlalchemy import select, join
from sqlalchemy.sql import func

with Session(engine) as session:
    db_session = session


def db_register_user(full_name, chat_id):
    """регистрация юзера в дб"""
    try:
        query = Users(name=full_name, telegram=chat_id)
        db_session.add(query)
        db_session.commit()
        return False
    except IntegrityError:
        db_session.rollback()
        return True


def db_update_user(chat_id, phone: str):
    """номер телефона юзера, номера строкового типа"""
    query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
    db_session.execute(query)
    db_session.commit()


def db_create_user_cart(chat_id):
    """создание корзины юзера, ограничение: 1 юзер=1 корзина, а также отсутствие возможности
    анонимно создавать корзину"""
    try:
        subquery = db_session.scalar(select(Users).where(Users.telegram == chat_id))
        query = Carts(user_id=subquery.id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        db_session.rollback()
    except AttributeError:
        db_session.rollback()


def db_get_all_category():
    """получение всех категорий"""
    query = select(Categories)
    return db_session.scalars(query)


def db_get_finally_price(chat_id):
    """получение итоговой цены"""
    query = select(func.sum(FinallyCarts.final_price)). \
        select_from(
        join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)
    ). \
        join(Users, Users.id == Carts.user_id). \
        where(Users.telegram == chat_id)

    return db_session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id: int, limit: int = 5):
    """получить последние заказы пользователя"""
    query = (
        select(FinallyCarts)
        .join(Carts, FinallyCarts.cart_id == Carts.id)
        .join(Users, Users.id == Carts.user_id)
        .where(Users.telegram == chat_id)
        .order_by(FinallyCarts.id.desc())
        .limit(limit)
    )
    return db_session.scalars(query).all()


def db_get_cart_items(chat_id: int):
    """получить все товары текущей корзины пользователя"""
    query = (
        select(FinallyCarts)
        .join(Carts, FinallyCarts.cart_id == Carts.id)
        .join(Users, Users.id == Carts.user_id)
        .where(Users.telegram == chat_id)
    )
    return db_session.scalars(query).all()


def db_get_product(category_id):
    """получение продуктов по id категории"""
    query = select(Products).where(Products.category_id == category_id)
    return db_session.scalars(query)


def db_add_products(products_data: list[dict]):
    """добавление нескольких товаров в БД, использовал для доп. добавления товаров, прямо из модуля"""
    try:
        for data in products_data:
            category = db_session.scalar(
                select(Categories).where(Categories.category_name == data["category_name"])
            )
            if not category:
                print(f"Категория {data['category_name']} не найдена.")
                continue

            product = Products(
                product_name=data["product_name"],
                description=data["description"],
                image=data["image"],
                price=data["price"],
                category_id=category.id
            )
            db_session.add(product)

        db_session.commit()
        print("Продукты успешно добавлены.")

    except IntegrityError as e:
        db_session.rollback()
        print(f"Ошибка добавления: {e}")


def db_get_product_by_id(product_id: int) -> Products:
    """получение продукта по его id"""
    query = select(Products).where(Products.id == product_id)
    return db_session.scalar(query)


def db_get_user_cart(chat_id: int) -> Carts:
    """получение корзины пользователя по его id"""
    query = select(Carts).join(Users).where(Users.telegram == chat_id)
    return db_session.scalar(query)


def db_update_to_cart(price: DECIMAL, cart_id: int, quantity=1) -> None:
    """обновление корзины пользователя по его id"""
    query = update(Carts).where(Carts.id == cart_id).values(total_price=price, total_products=quantity)
    db_session.execute(query)
    db_session.commit()

# if __name__ == "__main__":
#     products = [
#         {
#             "product_name": "Овсяное печенье",
#             "description": "Домашнее овсяное печенье",
#             "image": "media/cookies/ovsyanoe.jpg",
#             "price": 15.50,
#             "category_name": "Печенье"
#         },
#         {
#             "product_name": "Шоколадное печенье",
#             "description": "Печенье с кусочками шоколада",
#             "image": "media/cookies/choco_cookie.jpg",
#             "price": 22.00,
#             "category_name": "Печенье"
#         },
#         {
#             "product_name": "Кокосовое печенье",
#             "description": "С хрустящей корочкой и кокосовой стружкой",
#             "image": "media/cookies/kokos_cookie.jpg",
#             "price": 28.00,
#             "category_name": "Печенье"
#         }
#     ]
#
#     db_add_products(products)
