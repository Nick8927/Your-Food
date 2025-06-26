from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select, DECIMAL, join
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from database.models import Users, Categories, Products, Carts, FinallyCarts, Orders
from database.base import engine


def get_session():
    return Session(engine)


def db_register_user(full_name, chat_id):
    """регистрация юзера в дб"""
    try:
        with get_session() as session:
            query = Users(name=full_name, telegram=chat_id)
            session.add(query)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_update_user(chat_id, phone: str):
    """номер телефона юзера, номера строкового типа"""
    with get_session() as session:
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id):
    """создание корзины юзера, ограничение: 1 юзер=1 корзина"""
    try:
        with get_session() as session:
            subquery = session.scalar(select(Users).where(Users.telegram == chat_id))
            query = Carts(user_id=subquery.id)
            session.add(query)
            session.commit()
            return True
    except IntegrityError:
        return False
    except AttributeError:
        return False


def db_get_all_category():
    """получение всех категорий"""
    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """получение итоговой цены"""
    with get_session() as session:
        query = (
            select(func.sum(FinallyCarts.final_price))
            .select_from(join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id))
            .join(Users, Users.id == Carts.user_id)
            .where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id: int, limit: int = 5):
    """получить последние заказы пользователя из таблицы orders"""
    with get_session() as session:
        query = (
            select(Orders)
            .join(Carts, Orders.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .where(Users.telegram == chat_id)
            .order_by(Orders.id.desc())
            .limit(limit)
        )
        return session.scalars(query).all()


def db_get_cart_items(chat_id: int):
    """получить все товары текущей корзины пользователя"""
    with get_session() as session:
        query = (
            select(FinallyCarts)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Users.id == Carts.user_id)
            .where(Users.telegram == chat_id)
        )
        return session.scalars(query).all()


def db_get_product(category_id):
    """получение продуктов по id категории"""
    with get_session() as session:
        query = select(Products).where(Products.category_id == category_id)
        return session.scalars(query).all()


def db_add_products(products_data: list[dict]):
    """добавление нескольких товаров в БД"""
    try:
        with get_session() as session:
            for data in products_data:
                category = session.scalar(
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
                session.add(product)

            session.commit()
            print("Продукты успешно добавлены.")
    except IntegrityError as e:
        print(f"Ошибка добавления: {e}")


def db_get_product_by_id(product_id: int) -> Products:
    """получение продукта по его id"""
    with get_session() as session:
        query = select(Products).where(Products.id == product_id)
        return session.scalar(query)


def db_get_product_by_name(product_name: str) -> Products:
    """получение продукта по его имени"""
    with get_session() as session:
        query = select(Products).where(Products.product_name == product_name)
        return session.scalar(query)


def db_get_user_cart(chat_id: int) -> Carts:
    """получение корзины пользователя по его id"""
    with get_session() as session:
        query = select(Carts).join(Users).where(Users.telegram == chat_id)
        return session.scalar(query)


def db_update_to_cart(price: DECIMAL, cart_id: int, quantity=1) -> None:
    """обновление корзины пользователя по его id"""
    with get_session() as session:
        query = update(Carts).where(Carts.id == cart_id).values(total_price=price, total_products=quantity)
        session.execute(query)
        session.commit()


def db_update_product_image(product_name: str, new_image_path: str):
    """обновление изображения товара"""
    with get_session() as session:
        product = session.scalar(select(Products).where(Products.product_name == product_name))
        if not product:
            return
        product.image = new_image_path
        session.commit()


def db_upsert_final_cart_item(cart_id, product_name, total_price, total_products):
    """
    Добавляет товар в финальную корзину или обновляет его, если уже есть.
    Возвращает статус: 'inserted', 'updated' или 'error'
    """
    try:
        with get_session() as session:
            item = (
                session.query(FinallyCarts)
                .filter_by(cart_id=cart_id, product_name=product_name)
                .first()
            )

            if item:
                item.quantity = total_products
                item.final_price = total_price
                session.commit()
                return 'updated'

            new_item = FinallyCarts(
                cart_id=cart_id,
                product_name=product_name,
                quantity=total_products,
                final_price=total_price
            )
            session.add(new_item)
            session.commit()
            return 'inserted'

    except Exception as e:
        print(f"[db_upsert_cart_item] Ошибка: {e}")
        return 'error'


def db_get_final_cart_items(chat_id: int):
    """получение всех товаров в финальной корзине"""
    with get_session() as session:
        query = select(
            FinallyCarts.product_name,
            FinallyCarts.quantity,
            FinallyCarts.final_price,
            FinallyCarts.cart_id
        ).join(Carts).join(Users).where(Users.telegram == chat_id)
        return session.execute(query).fetchall()


def db_get_product_for_delete(chat_id: int):
    """удаление товаров из корзины"""
    with get_session() as session:
        query = (
            select(FinallyCarts.id, FinallyCarts.product_name)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchall()


def db_increase_product_quantity(finally_cart_id: int):
    """увеличение количества товара в корзине"""
    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity += 1
        item.final_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_decrease_product_quantity(finally_cart_id: int):
    """уменьшение количества товара в корзине"""
    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False

        product = session.execute(
            select(Products).where(Products.product_name == item.product_name)).scalar_one_or_none()
        if not product:
            return False

        item.quantity -= 1

        if item.quantity <= 0:
            session.delete(item)
        else:
            item.final_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_clear_final_cart(chat_id: int):
    """Удаление всех товаров из финальной корзины пользователя"""
    cart = db_get_user_cart(chat_id)
    if not cart:
        return

    with get_session() as session:
        query = delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id)
        session.execute(query)
        session.commit()


def db_save_order_history(chat_id: int):
    """Сохраняет текущую финальную корзину в таблицу заказов"""
    cart = db_get_user_cart(chat_id)
    if not cart:
        return

    with get_session() as session:
        final_items = session.query(FinallyCarts).filter_by(cart_id=cart.id).all()

        for item in final_items:
            session.add(
                Orders(
                    cart_id=cart.id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    final_price=item.final_price
                )
            )

        session.commit()


def db_get_user_phone(chat_id: int) -> str:
    """Получение номера телефона пользователя по Telegram ID"""
    with get_session() as session:
        query = select(Users.phone).where(Users.telegram == chat_id)
        return session.execute(query).fetchone()[0]


def db_update_user_language(telegram_id: int, language: str):
    """Обновляет язык пользователя в БД """
    with get_session() as session:
        session.execute(
            update(Users).where(Users.telegram == telegram_id).values(language=language)
        )
        session.commit()
