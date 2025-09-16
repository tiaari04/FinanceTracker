from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

# for API POST reuqests
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    date: date
    description: str

class TransactionCreate(TransactionBase):
    category: str

# for API responses
class Transaction(BaseModel):
    transaction_id: int
    amount: float
    date: date
    description: Optional[str] = None
    category_id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    data: list[Transaction]