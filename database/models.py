from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DECIMAL

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_ADDRESS = getenv("HOST")
DB_NAME = getenv("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}: {DB_PASSWORD}@{DB_ADDRESS}", echo=True)


class Base(DeclarativeBase):
    pass


class Users(Base):
    """хранение информации о пользователях бота"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    carts: Mapped[int] = relationship("Carts", back_populates='user_cart')

    def __str__(self):
        return self.name


class Carts(Base):
    """корзина товаров пользователей"""
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(5, 2), default=0)
    total_products: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user_cart: Mapped[Users] = relationship(back_populates="carts")
    finally_id: Mapped[int] = relationship("Finally_carts", back_populates="user_cart")

    def __str__(self):
        return str(self.id)


class Finally_carts(Base):
    """итоговая корзина для товаров на оплату"""
    __tablename__ = "finnaly_carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    final_price: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    quantity: Mapped[int]

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    user_cart: Mapped[Carts] = relationship(back_populates="finally_id")

    __table_args__ = (UniqueConstraint("cart_id", "product_name"),)

    def __str__(self):
        return str(self.id)


class Categories(Base):
    """категории продуктов"""
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String[25], unique=True)

    products: Mapped['Products'] = relationship('product_category')

    def __str__(self):
        return self.category_name


class Products(Base):
    """перечень продуктов"""
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(25), unique=True)
    description: Mapped[str]
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    product_category: Mapped[Categories] = relationship('products')
