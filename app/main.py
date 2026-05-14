"""
FastAPI Main Application - Shopee Mini Order Management System
Hệ thống quản lý đơn hàng với RabbitMQ & Redis
"""
from fastapi import FastAPI, HTTPException
from datetime import datetime
from .database import Base, engine, SessionLocal
from .schemas import OrderCreate
from .invoice_schemas import InvoiceCreate, InvoiceResponse
from .producer import publish_order, get_queue_stats
from .services.order_service import create_order, get_all_orders, get_order_by_id, update_order_status
from .services.invoice_service import (
    create_invoice, get_invoice_by_id, get_all_invoices,
    get_invoices_by_customer, get_invoice_by_order_id,
    update_invoice_status, get_invoice_statistics, print_invoice_detail
)
from .services.product_service import seed_products

# Khởi tạo FastAPI
app = FastAPI(
    title="Shopee Mini - Order Management API",
    version="1.0.0",
    description="Hệ thống quản lý đơn hàng với RabbitMQ & Redis"
)

# Tạo database tables
Base.metadata.create_all(bind=engine)

# Seed dữ liệu sản phẩm mẫu
db = SessionLocal()
seed_products(db)


# =========================
# Health Check Endpoints
# =========================

@app.get("/")
def home():
    """Kiểm tra API"""
    return {
        "message": "Shopee Mini API is running ✅",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# =========================
# Product Endpoints
# =========================

@app.get("/products")
def get_products():
    """Lấy danh sách tất cả sản phẩm"""
    db = SessionLocal()
    from .models import Product
    
    products = db.query(Product).all()
    
    return {
        "total": len(products),
        "products": products
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Lấy thông tin sản phẩm"""
    db = SessionLocal()
    from .models import Product
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


# =========================
# Order Endpoints
# =========================

@app.post("/orders")
def create_new_order(order: OrderCreate):
    """Tạo đơn hàng mới"""
    db = SessionLocal()
    
    # Tạo order trong DB
    new_order = create_order(
        db=db,
        customer=order.customer,
        product_id=order.product_id,
        quantity=order.quantity
    )
    
    # Gửi order vào RabbitMQ
    publish_order({
        "id": new_order.id,
        "customer": new_order.customer,
        "product_id": new_order.product_id,
        "product": {
            "id": new_order.product_id,
            "name": "Product"
        },
        "quantity": new_order.quantity,
        "status": new_order.status,
        "process_time": 3,
        "created_at": datetime.now().isoformat()
    })
    
    return {
        "message": "Order created and sent to queue ✅",
        "order_id": new_order.id,
        "status": new_order.status,
        "customer": new_order.customer
    }


@app.get("/orders")
def get_orders():
    """Lấy danh sách tất cả đơn hàng"""
    db = SessionLocal()
    
    orders = get_all_orders(db)
    
    return {
        "total": len(orders),
        "orders": orders
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    """Lấy thông tin đơn hàng"""
    db = SessionLocal()
    
    order = get_order_by_id(db, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@app.patch("/orders/{order_id}/status")
def update_order(order_id: int, status: str):
    """Cập nhật trạng thái đơn hàng"""
    db = SessionLocal()
    
    # Kiểm tra status hợp lệ
    valid_statuses = ["Pending", "Processing", "Completed", "Failed"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    updated_order = update_order_status(db, order_id, status)
    
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "message": "Order status updated ✅",
        "order_id": order_id,
        "status": updated_order.status
    }


# =========================
# Queue Status Endpoints
# =========================

@app.get("/queue/status")
def get_queue_status():
    """Lấy thống kê hàng đợi"""
    stats = get_queue_stats()
    
    if stats:
        return {
            "queue_name": "order_queue",
            "messages_pending": stats["message_count"],
            "active_consumers": stats["consumer_count"],
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {
            "error": "Could not retrieve queue stats"
        }


@app.post("/queue/clear")
def clear_queue():
    """Xóa tất cả đơn hàng trong hàng đợi"""
    from .producer import purge_queue
    
    purge_queue()
    
    return {
        "message": "Queue cleared ✅",
        "timestamp": datetime.now().isoformat()
    }


# =========================
# Invoice Endpoints (Hóa Đơn)
# =========================

@app.post("/invoices")
def create_new_invoice(invoice_data: InvoiceCreate):
    """Tạo hóa đơn mới"""
    db = SessionLocal()
    
    # Kiểm tra order có tồn tại
    order = get_order_by_id(db, invoice_data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Tạo hóa đơn
    new_invoice = create_invoice(
        db=db,
        order_id=invoice_data.order_id,
        customer=invoice_data.customer,
        product_name=invoice_data.product_name,
        quantity=invoice_data.quantity,
        unit_price=invoice_data.unit_price
    )
    
    return {
        "message": "Invoice created successfully ✅",
        "invoice_id": new_invoice.id,
        "invoice_number": new_invoice.invoice_number,
        "total_amount": new_invoice.total_amount
    }


@app.get("/invoices")
def get_invoices():
    """Lấy danh sách tất cả hóa đơn"""
    db = SessionLocal()
    
    invoices = get_all_invoices(db)
    
    return {
        "total": len(invoices),
        "invoices": invoices
    }


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    """Lấy chi tiết hóa đơn"""
    db = SessionLocal()
    
    invoice = get_invoice_by_id(db, invoice_id)
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice


@app.get("/invoices/by-order/{order_id}")
def get_invoice_for_order(order_id: int):
    """Lấy hóa đơn của một đơn hàng"""
    db = SessionLocal()
    
    invoice = get_invoice_by_order_id(db, order_id)
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for this order")
    
    return invoice


@app.get("/invoices/customer/{customer}")
def get_customer_invoices(customer: str):
    """Lấy tất cả hóa đơn của khách hàng"""
    db = SessionLocal()
    
    invoices = get_invoices_by_customer(db, customer)
    
    return {
        "customer": customer,
        "total_invoices": len(invoices),
        "invoices": invoices
    }


@app.patch("/invoices/{invoice_id}/status")
def update_invoice(invoice_id: int, status: str):
    """Cập nhật trạng thái hóa đơn"""
    db = SessionLocal()
    
    valid_statuses = ["Active", "Paid", "Cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    updated_invoice = update_invoice_status(db, invoice_id, status)
    
    if not updated_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return {
        "message": "Invoice status updated ✅",
        "invoice_id": invoice_id,
        "status": updated_invoice.status
    }


@app.get("/invoices/stats/summary")
def get_invoices_statistics():
    """Lấy thống kê hóa đơn"""
    db = SessionLocal()
    
    stats = get_invoice_statistics(db)
    
    return {
        "statistics": stats,
        "timestamp": datetime.now().isoformat()
    }


# =========================
# System Info Endpoints
# =========================

@app.get("/system/info")
def get_system_info():
    """Lấy thông tin hệ thống"""
    db = SessionLocal()
    from .models import Order, Invoice
    
    total_orders = db.query(Order).count()
    completed_orders = db.query(Order).filter(Order.status == "Completed").count()
    pending_orders = db.query(Order).filter(Order.status == "Pending").count()
    
    total_invoices = db.query(Invoice).count()
    invoice_stats = get_invoice_statistics(db)
    
    return {
        "system": "Shopee Mini Order Management System",
        "version": "1.0.0",
        "database": {
            "total_orders": total_orders,
            "completed": completed_orders,
            "pending": pending_orders,
            "total_invoices": total_invoices,
            "total_revenue": invoice_stats["total_revenue"]
        },
        "timestamp": datetime.now().isoformat()
    }
