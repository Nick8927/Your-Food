from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


class ProductAddons(Base):
    __tablename__ = "product_addons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(default=0)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))

    product = relationship("Products", back_populates="addons")


class CartAddons(Base):
    __tablename__ = "cart_addons"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    addon_id: Mapped[int] = mapped_column(ForeignKey("product_addons.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(default=0)

    cart = relationship("Carts", back_populates="addons")
    addon = relationship("ProductAddons")


class OrderAddons(Base):
    __tablename__ = "order_addons"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]

    order = relationship("Orders", back_populates="addons")