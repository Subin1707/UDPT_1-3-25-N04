"""
Order Generator - Tạo danh sách đơn hàng mẫu
Tạo 10-20 đơn hàng với thông tin ngẫu nhiên
"""
import random
from datetime import datetime

# =========================
# Dữ liệu mẫu
# =========================
CUSTOMERS = [
    "Nguyễn Văn A",
    "Trần Thị B",
    "Lê Quốc C",
    "Phạm Minh D",
    "Hoàng Anh E",
    "Võ Tuấn F",
    "Bùi Thanh G",
    "Đặng Huy H",
]

PRODUCTS = [
    {"id": 1, "name": "iPhone 16"},
    {"id": 2, "name": "MacBook Pro M4"},
    {"id": 3, "name": "AirPods Pro"},
    {"id": 4, "name": "Mechanical Keyboard"},
    {"id": 5, "name": "Gaming Mouse"},
]


# =========================
# Generate Orders
# =========================
def generate_orders(num_orders: int = 15) -> list:
    """
    Tạo danh sách đơn hàng ngẫu nhiên
    
    Args:
        num_orders: Số lượng đơn hàng cần tạo (10-20)
    
    Returns:
        Danh sách các đơn hàng
    """
    if num_orders < 10 or num_orders > 20:
        num_orders = 15
    
    orders = []
    
    for i in range(1, num_orders + 1):
        order = {
            "id": i,
            "customer": random.choice(CUSTOMERS),
            "product": random.choice(PRODUCTS),
            "quantity": random.randint(1, 5),
            "process_time": random.randint(1, 5),  # 1-5 giây
            "status": "Pending",
            "created_at": datetime.now().isoformat()
        }
        orders.append(order)
    
    return orders


# =========================
# Print Orders
# =========================
def print_orders(orders: list):
    """In danh sách đơn hàng"""
    print("\n" + "="*60)
    print(f"📋 DANH SÁCH {len(orders)} ĐƠN HÀNG")
    print("="*60)
    
    for order in orders:
        print(f"\n Đơn #{order['id']:<3} | {order['customer']:<15} | "
              f"{order['product']['name']:<20} | "
              f"SL: {order['quantity']} | "
              f"Thời gian: {order['process_time']}s")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Tạo 15 đơn hàng mẫu
    orders = generate_orders(15)
    print_orders(orders)
