from pydantic import BaseModel
from typing import Optional


# =========================
# Product Schema
# =========================
class ProductBase(BaseModel):
    name: str
    stock: int
    price: int


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# Order Schema
# =========================
class OrderCreate(BaseModel):
    customer: str
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    customer: str
    product_id: int
    quantity: int
    status: str

    class Config:
        from_attributes = True