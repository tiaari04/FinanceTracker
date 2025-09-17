from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id: Mapped[str] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[int] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False, default=date.today())
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.category_id"))

    # relationship to Transaction
    category: Mapped["Category"] = relationship(back_populates="transactions")

class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # relationship to Category
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

