from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


# =========================
# Product Model
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Tên sản phẩm
    name = Column(String, nullable=False)

    # Số lượng tồn kho
    stock = Column(Integer, default=0)

    # Giá sản phẩm
    price = Column(Integer, default=0)


# =========================
# Order Model
# =========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Tên khách hàng
    customer = Column(String, nullable=False)

    # ID sản phẩm
    product_id = Column(Integer, nullable=False)

    # Số lượng mua
    quantity = Column(Integer, nullable=False)

    # Trạng thái đơn hàng
    # Pending / Processing / Completed
    status = Column(
        String,
        default="Pending"
    )


# =========================
# Invoice Model (Hóa Đơn)
# =========================
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    # ID đơn hàng
    order_id = Column(Integer, nullable=False)

    # Mã hóa đơn (HĐ-001, HĐ-002, ...)
    invoice_number = Column(String, nullable=False, unique=True)

    # Tên khách hàng
    customer = Column(String, nullable=False)

    # Tên sản phẩm
    product_name = Column(String, nullable=False)

    # Số lượng
    quantity = Column(Integer, nullable=False)

    # Đơn giá
    unit_price = Column(Float, default=0)

    # Thành tiền (quantity * unit_price)
    total_amount = Column(Float, default=0)

    # Trạng thái hóa đơn
    status = Column(String, default="Active")

    # Ngày tạo hóa đơn
    created_at = Column(DateTime, default=datetime.now)

    # Ngày cập nhật
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)