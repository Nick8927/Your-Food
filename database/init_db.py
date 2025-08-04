from sqlalchemy.orm import Session
from sqlalchemy import text, select
from database.base import engine, Base
from database.models import Categories, Products
from database.models.orders import Orders

def init_db():
    with engine.connect() as conn:
        # conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print("Создаём таблицы...")
    Base.metadata.create_all(engine)

    categories = ("Торты", "Печенье")
    products = (
        ("Торты", "Медовик", 45, "мед, мука, сахар, яйца, масло", "media/cakes/hone_cake.jpg"),
        ("Торты", "Наполеон", 55, "молоко, мука, сахар, яйца, масло", "media/cakes/cake_napoleon.jpg"),
        ("Торты", "Птичье молоко", 45, "желатин, мука, сахар, яйца, масло", "media/cakes/cake_milk.jpg"),
        ("Печенье", "Шоколадное печенье", 20, "шоколад, мука, сахар, яйца, масло", "media/cookies/choco_cookie.jpg"),
        ("Печенье", "Кокосовое печенье", 25, "кокос, мука, сахар, яйца, масло", "media/cookies/kokos_cookie.jpg"),
        ("Печенье", "Овсяное печенье", 15, "овсянка, мука, сахар, яйца, масло", "media/cookies/ovsyanoe.jpg"),
    )

    with Session(engine) as session:
        category_map = {}


        for name in categories:
            category = session.scalar(select(Categories).where(Categories.category_name == name))
            if not category:
                category = Categories(category_name=name)
                session.add(category)
                session.flush()
            category_map[name] = category.id


        for category_name, name, price, desc, image in products:
            product_exists = session.scalar(select(Products).where(Products.product_name == name))
            if product_exists:
                continue

            category_id = category_map.get(category_name)
            if category_id:
                product = Products(
                    category_id=category_id,
                    product_name=name,
                    price=price,
                    description=desc,
                    image=image
                )
                session.add(product)

        session.commit()
        print("База успешно инициализирована")

if __name__ == "__main__":
    init_db()