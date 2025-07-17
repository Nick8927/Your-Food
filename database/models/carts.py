from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from .product_addons import CartAddons
from .users import Users


class Carts(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(10, 2), default=0)
    total_products: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user_cart: Mapped["Users"] = relationship(back_populates="carts")
    finally_id: Mapped[int] = relationship("FinallyCarts", back_populates="user_cart")
    addons: Mapped[list[CartAddons]] = relationship("CartAddons", back_populates="cart", cascade="all, delete-orphan")


    def __str__(self):
        return str(self.id)


class FinallyCarts(Base):
    __tablename__ = "finally_carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    final_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    quantity: Mapped[int]

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    user_cart: Mapped[Carts] = relationship(back_populates="finally_id")

    __table_args__ = (
        {'sqlite_autoincrement': True},
    )

    def __str__(self):
        return str(self.id)