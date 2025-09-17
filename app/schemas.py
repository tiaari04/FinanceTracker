import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    category_id: int

    model_config = ConfigDict(from_attributes=True)

# for API POST reuqests
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    date: Optional[datetime.date] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    category: str

# for API responses
class TransactionResponse(BaseModel):
    transaction_id: int
    amount: float
    date: datetime.date
    description: Optional[str] = None
    category_id: int
    category: Category

    model_config = ConfigDict(from_attributes=True)
