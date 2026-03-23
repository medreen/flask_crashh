#SQLAlchemy is an ORM.Object Relational Mapper
#Helps execute queries using methods.
#Define the table structure using classes and objects.

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
# from datetime import datetime

class Base(DeclarativeBase):
    pass

#Map users table to User class
class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)

class Authentication(Base):
    __tablename__ = "user_authentication"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    