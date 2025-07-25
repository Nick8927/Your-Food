from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from .categories import Categories
from .product_addons import ProductAddons


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(25), unique=True)
    description: Mapped[str]
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    addons: Mapped[list["ProductAddons"]] = relationship("ProductAddons", back_populates="product")
    product_category: Mapped["Categories"] = relationship(back_populates='products')