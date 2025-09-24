import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from app.models import Transaction

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

class TransactionListResponse(BaseModel):
    data: list[TransactionResponse]

# for OData GET requests
class TransactionsGet(BaseModel):
    filter: Optional[str] = Field(None, alias="$filter")
    orderby: Optional[str] = Field(None, alias="$orderby")
    top: Optional[str] = Field(None, alias="$top")
    skip: Optional[str] = Field(None, alias="$skip")
    expand: Optional[str] = Field(None, alias="$expand")

class TransactionFilter(Filter):
    amount: Optional[float] = None
    amount__gt: Optional[float] = None
    amount__lt: Optional[float] = None
    date__lt: Optional[datetime.date] = None
    date__gt: Optional[datetime.date] = None
    date: Optional[datetime.date] = None
    category_id: Optional[int] = None
    category_id__neq: Optional[int] = None
    
    class Constants(Filter.Constants):
        model = Transaction # The SQLAlchemy model to filter on
