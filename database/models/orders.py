from sqlalchemy import String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_name: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int]
    final_price: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))

    def __str__(self):
        return f"{self.product_name} x{self.quantity} — {self.final_price} руб"
