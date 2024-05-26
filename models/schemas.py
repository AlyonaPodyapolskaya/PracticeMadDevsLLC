from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

# Pydantic схемы для чтения (response)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class StoreResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]


class BrandResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    store_id: int
    brand_id: int


class PaymentResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    user_id: int
    product_id: int
    store_id: int


class StatisticResponse(BaseModel):
    id: int
    event_type: str
    event_time: datetime
    user_id: int
    product_id: int
    store_id: int


# Pydantic схемы для создания (create)

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str


class StoreCreate(BaseModel):
    name: str
    description: Optional[str]


class BrandCreate(BaseModel):
    name: str
    description: Optional[str]


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    store_id: int
    brand_id: int


class PaymentCreate(BaseModel):
    amount: float
    description: Optional[str]
    user_id: int
    product_id: int
    store_id: int


class StatisticCreate(BaseModel):
    event_type: str
    event_time: datetime
    user_id: int
    product_id: int
    store_id: int
