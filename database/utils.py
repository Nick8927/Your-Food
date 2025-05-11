from typing import Iterable
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select, DECIMAL
from sqlalchemy.sql.functions import sum
from sqlalchemy.exc import IntegrityError
from database.models import Users, Categories, Products, Carts, FinallyCarts
from .base import engine
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
    query = select(func.sum(FinallyCarts.final_price)).\
        select_from(
            join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)
        ).\
        join(Users, Users.id == Carts.user_id).\
        where(Users.telegram == chat_id)

    return db_session.execute(query).fetchone()[0]
