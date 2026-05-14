"""
Invoice Schema - Pydantic models cho hóa đơn
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# =========================
# Invoice Schemas
# =========================
class InvoiceCreate(BaseModel):
    """Schema tạo hóa đơn"""
    order_id: int
    customer: str
    product_name: str
    quantity: int
    unit_price: float


class InvoiceResponse(BaseModel):
    """Schema response hóa đơn"""
    id: int
    order_id: int
    invoice_number: str
    customer: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceDetail(BaseModel):
    """Chi tiết hóa đơn"""
    invoice_number: str
    customer: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceStatistics(BaseModel):
    """Thống kê hóa đơn"""
    total_invoices: int
    active_invoices: int
    total_revenue: float
    average_value: float
