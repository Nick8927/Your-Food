from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select, DECIMAL, join, func
from sqlalchemy.exc import IntegrityError

from database.base import engine
from database.models import (Users, Categories, Products, Carts,
                             FinallyCarts, Orders, ProductAddons, CartAddons,
                             OrderAddons)


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
    """получаем финальную сумму заказа: товары + добавки"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users, Users.id == Carts.user_id)
            .filter(Users.telegram == chat_id)
            .first()
        )
        if not cart:
            return 0.0

        product_total = (
            session.query(func.coalesce(func.sum(FinallyCarts.final_price), 0))
            .filter(FinallyCarts.cart_id == cart.id)
            .scalar()
        )

        if product_total == 0:
            return 0.0

        addons_total = (
            session.query(func.coalesce(func.sum(CartAddons.price), 0))
            .filter(CartAddons.cart_id == cart.id)
            .scalar()
        )

        return float(product_total + addons_total)


def db_get_last_orders(chat_id: int, limit: int = 5):
    """получить последние заказы пользователя из таблицы orders + addons"""
    with get_session() as session:
        orders = (
            session.query(Orders)
            .join(Carts, Orders.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .filter(Users.telegram == chat_id)
            .order_by(Orders.id.desc())
            .limit(limit)
            .all()
        )

        result = []
        for order in orders:
            addons = (
                session.query(OrderAddons)
                .filter(OrderAddons.order_id == order.id)
                .all()
            )
            result.append({
                "order": order,
                "addons": addons
            })

        return result


def db_get_cart_items(chat_id: int):
    """получение всех товаров в корзине"""
    with get_session() as session:
        query = (
            select(
                FinallyCarts.id,
                FinallyCarts.product_name,
                FinallyCarts.final_price,
                FinallyCarts.quantity,
                FinallyCarts.cart_id,
                func.coalesce(func.sum(CartAddons.price), 0).label("addons_total")
            )
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Users.id == Carts.user_id)
            .outerjoin(CartAddons, CartAddons.cart_id == Carts.id)
            .where(Users.telegram == chat_id)
            .group_by(FinallyCarts.id)
        )
        return session.execute(query).mappings().all()


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


def db_update_product_image(product_name: str, new_image_path: str):
    """обновление изображения товара"""
    with get_session() as session:
        product = session.scalar(select(Products).where(Products.product_name == product_name))
        if not product:
            return
        product.image = new_image_path
        session.commit()


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


def db_get_user_phone(chat_id: int):
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


def db_delete_user_by_telegram_id(chat_id: int):
    """Удаление пользователя по Telegram ID"""
    try:
        with get_session() as session:
            user = session.scalar(select(Users).where(Users.telegram == chat_id))
            if not user:
                return False

            cart = session.scalar(select(Carts).where(Carts.user_id == user.id))

            if cart:
                session.execute(delete(Orders).where(Orders.cart_id == cart.id))
                session.execute(delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id))
                session.execute(delete(Carts).where(Carts.id == cart.id))

            session.execute(delete(Users).where(Users.id == user.id))
            session.commit()
            return True

    except Exception as e:
        print(f"[db_delete_user_by_telegram_id] Ошибка: {e}")
        return False


def db_get_addons_by_product(product_id: int):
    """Получить добавки для конкретного продукта"""
    with get_session() as session:
        product = session.get(Products, product_id)
        if not product:
            return []

        CAKE_CATEGORY_ID = 1
        if product.category_id != CAKE_CATEGORY_ID:
            return []

        query = select(ProductAddons).where(ProductAddons.product_id == product_id)
        return session.scalars(query).all()


def db_get_cart_addons_by_cart_id(cart_id: int):
    """Получить добавки, выбранные пользователем для конкретного cart_id"""
    with get_session() as session:
        query = select(CartAddons).where(CartAddons.cart_id == cart_id)
        return session.scalars(query).all()


def db_get_addon_by_id(addon_id: int) -> ProductAddons:
    """Получить добавку по id"""
    with get_session() as session:
        query = select(ProductAddons).where(ProductAddons.id == addon_id)
        return session.scalar(query)


def db_add_addon_to_cart(telegram_id: int, addon_id: int):
    """Добавить добавку в корзину пользователя"""
    with get_session() as session:
        addon = session.get(ProductAddons, addon_id)
        if not addon:
            return False

        product = session.get(Products, addon.product_id)
        if not product:
            return False

        CAKE_CATEGORY_ID = 1
        if product.category_id != CAKE_CATEGORY_ID:
            return False

        cart = (
            session.query(Carts)
            .join(Users)
            .filter(Users.telegram == telegram_id)
            .first()
        )
        if not cart:
            return False

        cart_addon = CartAddons(
            cart_id=cart.id,
            addon_id=addon.id,
            name=addon.name,
            price=addon.price
        )
        session.add(cart_addon)
        session.commit()
        return True


def db_get_addons_total_price(cart_id: int):
    """Получить сумму всех добавок в корзине"""
    with get_session() as session:
        result = (
            session.query(func.coalesce(func.sum(CartAddons.price), 0))
            .filter(CartAddons.cart_id == cart_id)
            .scalar()
        )
        return float(result)


def db_remove_addon_from_cart(telegram_id: int, addon_id: int):
    """Удалить добавку из корзины пользователя"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users)
            .filter(Users.telegram == telegram_id)
            .first()
        )
        if not cart:
            return False

        addon = (
            session.query(CartAddons)
            .filter(CartAddons.cart_id == cart.id, CartAddons.addon_id == addon_id)
            .first()
        )
        if not addon:
            return False

        session.delete(addon)
        session.commit()
        return True


def db_remove_all_addons_from_cart(user_telegram_id: int) -> bool:
    """Удалить все добавки из корзины пользователя по Telegram ID"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users, Carts.user_id == Users.id)
            .filter(Users.telegram == user_telegram_id)
            .first()
        )

        if not cart:
            return False

        session.query(CartAddons).filter(CartAddons.cart_id == cart.id).delete()
        session.commit()
        return True


def db_is_addon_in_cart(user_telegram_id: int, addon_id: int) -> bool:
    """Проверяет, есть ли добавка в корзине пользователя"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users, Users.id == Carts.user_id)
            .filter(Users.telegram == user_telegram_id)
            .first()
        )
        if not cart:
            return False

        exists = (
            session.query(CartAddons)
            .filter_by(cart_id=cart.id, addon_id=addon_id)
            .first()
        )
        return exists is not None


def db_clear_addons_if_cart_empty(user_telegram_id: int) -> None:
    """Удаляет все добавки, если корзина пуста"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users, Carts.user_id == Users.id)
            .filter(Users.telegram == user_telegram_id)
            .first()
        )

        if not cart:
            return

        products_in_cart = (
            session.query(FinallyCarts)
            .filter(FinallyCarts.cart_id == cart.id)
            .count()
        )

        if products_in_cart == 0:
            session.query(CartAddons).filter(CartAddons.cart_id == cart.id).delete()
            session.commit()


def db_save_order_with_addons(chat_id: int):
    """Сохраняет финальную корзину и добавки в историю заказов"""
    with get_session() as session:
        cart = (
            session.query(Carts)
            .join(Users)
            .filter(Users.telegram == chat_id)
            .first()
        )
        if not cart:
            return False

        final_items = session.query(FinallyCarts).filter_by(cart_id=cart.id).all()
        if not final_items:
            return False

        for item in final_items:
            new_order = Orders(
                cart_id=cart.id,
                product_name=item.product_name,
                quantity=item.quantity,
                final_price=item.final_price
            )
            session.add(new_order)
            session.flush()

            cart_addons = (
                session.query(CartAddons)
                .filter(CartAddons.cart_id == cart.id)
                .all()
            )

            for addon in cart_addons:
                order_addon = OrderAddons(
                    order_id=new_order.id,
                    name=addon.name,
                    price=addon.price
                )
                session.add(order_addon)

        session.commit()
        return True


def db_add_or_update_item(cart_id: int, product_name: str, product_price: DECIMAL, increment: int = 0):
    """ Добавляет товар в finally_carts или обновляет его количество.
    Пересчитывает total_price и total_products в carts, включая addons."""
    try:
        with get_session() as session:
            item = (
                session.query(FinallyCarts)
                .filter_by(cart_id=cart_id, product_name=product_name)
                .first()
            )

            if item:
                if increment != 0:
                    item.quantity = max(1, item.quantity + increment)
                item.final_price = item.quantity * product_price
            else:
                qty = 1 if increment <= 0 else increment
                item = FinallyCarts(
                    cart_id=cart_id,
                    product_name=product_name,
                    quantity=qty,
                    final_price=qty * product_price
                )
                session.add(item)

            products_sum, total_products = session.query(
                func.coalesce(func.sum(FinallyCarts.final_price), 0),
                func.coalesce(func.sum(FinallyCarts.quantity), 0)
            ).filter(FinallyCarts.cart_id == cart_id).one()

            addons_sum = session.query(
                func.coalesce(func.sum(CartAddons.price), 0)
            ).filter(CartAddons.cart_id == cart_id).scalar()

            total_price = products_sum + addons_sum

            session.query(Carts).filter(Carts.id == cart_id).update({
                Carts.total_price: total_price,
                Carts.total_products: total_products
            })

            session.commit()
            return {
                "status": "ok",
                "total_price": float(total_price),
                "total_products": int(total_products),
                "product_quantity": item.quantity
            }

    except Exception as e:
        print(f"[db_add_or_update_item] Ошибка: {e}")
        return {"status": "error"}
