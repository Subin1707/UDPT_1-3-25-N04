from sqlalchemy.orm import Session
from ..models import Product


# =========================
# Seed Default Products
# =========================
def seed_products(db: Session):

    existing_products = db.query(Product).count()

    if existing_products > 0:
        return

    products = [
        Product(
            name="iPhone 16",
            stock=10,
            price=30000000
        ),

        Product(
            name="MacBook Pro M4",
            stock=5,
            price=55000000
        ),

        Product(
            name="AirPods Pro",
            stock=20,
            price=6000000
        ),

        Product(
            name="Mechanical Keyboard",
            stock=15,
            price=2500000
        ),

        Product(
            name="Gaming Mouse",
            stock=25,
            price=1200000
        )
    ]

    db.add_all(products)

    db.commit()

    print("Default products seeded")


# =========================
# Get All Products
# =========================
def get_all_products(db: Session):

    return db.query(Product).all()


# =========================
# Get Product By ID
# =========================
def get_product_by_id(
    db: Session,
    product_id: int
):

    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


# =========================
# Create Product
# =========================
def create_product(
    db: Session,
    name: str,
    stock: int,
    price: int
):

    product = Product(
        name=name,
        stock=stock,
        price=price
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product


# =========================
# Update Product Stock
# =========================
def update_product_stock(
    db: Session,
    product_id: int,
    quantity: int
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        return None

    # Trừ tồn kho
    product.stock -= quantity

    db.commit()

    db.refresh(product)

    return product


# =========================
# Delete Product
# =========================
def delete_product(
    db: Session,
    product_id: int
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        return False

    db.delete(product)

    db.commit()

    return True