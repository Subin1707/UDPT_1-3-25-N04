from sqlalchemy.orm import Session
from ..models import Order


# =========================
# Create Order
# =========================
def create_order(
    db: Session,
    customer: str,
    product_id: int,
    quantity: int
):

    order = Order(
        customer=customer,
        product_id=product_id,
        quantity=quantity,
        status="Pending"
    )

    db.add(order)

    db.commit()

    db.refresh(order)

    return order


# =========================
# Get All Orders
# =========================
def get_all_orders(db: Session):

    return db.query(Order).all()


# =========================
# Get Order By ID
# =========================
def get_order_by_id(
    db: Session,
    order_id: int
):

    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


# =========================
# Update Order Status
# =========================
def update_order_status(
    db: Session,
    order_id: int,
    status: str
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        return None

    order.status = status

    db.commit()

    db.refresh(order)

    return order


# =========================
# Delete Order
# =========================
def delete_order(
    db: Session,
    order_id: int
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        return False

    db.delete(order)

    db.commit()

    return True