"""
Invoice Service - Quản lý hóa đơn
"""
from sqlalchemy.orm import Session
from ..models import Invoice, Order
from datetime import datetime


# =========================
# Generate Invoice Number
# =========================
def generate_invoice_number(db: Session) -> str:
    """
    Tạo mã hóa đơn tự động
    Định dạng: HĐ-YYYYMMDD-XXXXXX
    VD: HĐ-20240514-000001
    """
    current_date = datetime.now()
    date_str = current_date.strftime("%Y%m%d")
    
    # Lấy số hóa đơn cùng ngày
    today_invoices = (
        db.query(Invoice)
        .filter(Invoice.invoice_number.like(f"HĐ-{date_str}-%"))
        .count()
    )
    
    invoice_seq = today_invoices + 1
    invoice_number = f"HĐ-{date_str}-{invoice_seq:06d}"
    
    return invoice_number


# =========================
# Create Invoice
# =========================
def create_invoice(
    db: Session,
    order_id: int,
    customer: str,
    product_name: str,
    quantity: int,
    unit_price: float
) -> Invoice:
    """
    Tạo hóa đơn mới từ đơn hàng
    
    Args:
        db: Database session
        order_id: ID của đơn hàng
        customer: Tên khách hàng
        product_name: Tên sản phẩm
        quantity: Số lượng
        unit_price: Đơn giá
    
    Returns:
        Invoice object
    """
    # Tính thành tiền
    total_amount = quantity * unit_price
    
    # Tạo mã hóa đơn
    invoice_number = generate_invoice_number(db)
    
    # Tạo đối tượng Invoice
    invoice = Invoice(
        order_id=order_id,
        invoice_number=invoice_number,
        customer=customer,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        total_amount=total_amount,
        status="Active"
    )
    
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    
    return invoice


# =========================
# Get Invoice By ID
# =========================
def get_invoice_by_id(
    db: Session,
    invoice_id: int
) -> Invoice:
    """Lấy hóa đơn theo ID"""
    return (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )


# =========================
# Get Invoice By Number
# =========================
def get_invoice_by_number(
    db: Session,
    invoice_number: str
) -> Invoice:
    """Lấy hóa đơn theo mã số"""
    return (
        db.query(Invoice)
        .filter(Invoice.invoice_number == invoice_number)
        .first()
    )


# =========================
# Get Invoice By Order ID
# =========================
def get_invoice_by_order_id(
    db: Session,
    order_id: int
) -> Invoice:
    """Lấy hóa đơn của một đơn hàng"""
    return (
        db.query(Invoice)
        .filter(Invoice.order_id == order_id)
        .first()
    )


# =========================
# Get All Invoices
# =========================
def get_all_invoices(db: Session):
    """Lấy tất cả hóa đơn"""
    return db.query(Invoice).all()


# =========================
# Get Invoices By Customer
# =========================
def get_invoices_by_customer(
    db: Session,
    customer: str
):
    """Lấy hóa đơn của khách hàng"""
    return (
        db.query(Invoice)
        .filter(Invoice.customer == customer)
        .all()
    )


# =========================
# Update Invoice Status
# =========================
def update_invoice_status(
    db: Session,
    invoice_id: int,
    status: str
) -> Invoice:
    """Cập nhật trạng thái hóa đơn"""
    invoice = get_invoice_by_id(db, invoice_id)
    
    if not invoice:
        return None
    
    invoice.status = status
    invoice.updated_at = datetime.now()
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


# =========================
# Get Invoice Statistics
# =========================
def get_invoice_statistics(db: Session) -> dict:
    """Lấy thống kê hóa đơn"""
    total_invoices = db.query(Invoice).count()
    total_revenue = 0
    
    invoices = db.query(Invoice).all()
    for invoice in invoices:
        total_revenue += invoice.total_amount
    
    active_invoices = (
        db.query(Invoice)
        .filter(Invoice.status == "Active")
        .count()
    )
    
    return {
        "total_invoices": total_invoices,
        "active_invoices": active_invoices,
        "total_revenue": total_revenue,
        "average_value": total_revenue / total_invoices if total_invoices > 0 else 0
    }


# =========================
# Print Invoice
# =========================
def print_invoice_detail(invoice: Invoice):
    """In chi tiết hóa đơn"""
    print("\n" + "="*60)
    print("📄 HÓA ĐƠN CHI TIẾT")
    print("="*60)
    print(f"Mã HĐ: {invoice.invoice_number}")
    print(f"Khách hàng: {invoice.customer}")
    print(f"Sản phẩm: {invoice.product_name}")
    print(f"Số lượng: {invoice.quantity}")
    print(f"Đơn giá: {invoice.unit_price:,.0f}₫")
    print(f"Thành tiền: {invoice.total_amount:,.0f}₫")
    print(f"Trạng thái: {invoice.status}")
    print(f"Ngày tạo: {invoice.created_at}")
    print("="*60 + "\n")
