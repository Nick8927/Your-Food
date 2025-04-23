from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, String, DECIMAL

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_ADDRESS = getenv("HOST")
DB_NAME = getenv("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}: {DB_PASSWORD}@{DB_ADDRESS}", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    """хранение информации о пользователях бота"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70))
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self):
        return self.name
