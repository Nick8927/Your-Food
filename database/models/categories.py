from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(25), unique=True)

    products = relationship('Products', back_populates='product_category')

    def __str__(self):
        return self.category_name