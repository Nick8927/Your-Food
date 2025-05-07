from .models import Categories,Carts,Finally_carts,Users,Products, engine
from sqlalchemy.orm import Session
from typing import Iterable
from sqlalchemy import select, update, delete
from sqlalchemy.sql.functions import sum
from sqlalchemy.exc import IntegrityError


with Session(engine) as session:
    db_session = session


