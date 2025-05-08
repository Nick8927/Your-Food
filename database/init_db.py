from sqlalchemy.orm import Session
from sqlalchemy import text
from database.base import engine, Base
from database.models import Categories, Products

def init_db():
    with engine.connect() as conn:
        # conn.execute(text("DROP SCHEMA public CASCADE"))

        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print("Создаём таблицы...")
    Base.metadata.create_all(engine)

    categories = ("Торты", "Печенье")
    products = (
        ("Торты", "Медовик", 45, "мед, мука, сахар, яйца, масло", "media/cakes/cake_milk"),
        ("Торты", "Наполеон", 55, "молоко, мука, сахар, яйца, масло", "media/cakes/cake_honey"),
        ("Торты", "Птичье молоко", 45, "желатин, мука, сахар, яйца, масло", "media/cakes/cake_napoleon"),
    )

    with Session(engine) as session:
        category_map = {}
        for name in categories:
            category = Categories(category_name=name)
            session.add(category)
            session.flush()
            category_map[name] = category.id

        for category_name, name, price, desc, image in products:
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

if __name__ == '__main__':
    init_db()
