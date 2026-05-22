from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    creator: Mapped[str | None] = mapped_column(String(50), nullable=True)
    modify_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    modifier: Mapped[str | None] = mapped_column(String(50), nullable=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salt: Mapped[str] = mapped_column(String(50), nullable=False)
    create_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    creator: Mapped[str | None] = mapped_column(String(50), nullable=True)
    modify_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    modifier: Mapped[str | None] = mapped_column(String(50), nullable=True)
