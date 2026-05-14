"""
Order Producer - Gửi đơn hàng vào RabbitMQ
Hỗ trợ:
- Gửi đơn hàng đơn lẻ
- Gửi batch đơn hàng
- Logging chi tiết
"""
import pika
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# =========================
# RabbitMQ Connection
# =========================
def get_connection():
    """Tạo kết nối RabbitMQ"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost"
        )
    )
    return connection


channel = None


def init_channel():
    """Khởi tạo channel"""
    global channel
    connection = get_connection()
    channel = connection.channel()
    
    # Tạo queue nếu chưa tồn tại
    channel.queue_declare(
        queue="order_queue",
        durable=True
    )
    
    print("✅ Kết nối RabbitMQ thành công")


# =========================
# Publish Single Order
# =========================
def publish_order(order_data: Dict[str, Any]):
    """
    Gửi một đơn hàng vào hàng đợi
    
    Args:
        order_data: Dữ liệu đơn hàng
    """
    global channel
    
    if channel is None:
        init_channel()
    
    try:
        channel.basic_publish(
            exchange="",
            routing_key="order_queue",
            body=json.dumps(order_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent message
                content_type='application/json'
            )
        )
        
        print(
            f"✅ [Producer] Gửi đơn #{order_data['id']} "
            f"({order_data['customer']}) vào hàng đợi"
        )
        
    except Exception as e:
        print(
            f"❌ [Producer] Lỗi gửi đơn #{order_data['id']}: {str(e)}"
        )


# =========================
# Publish Batch Orders
# =========================
def publish_orders_batch(orders: List[Dict[str, Any]], delay: float = 0.5):
    """
    Gửi batch đơn hàng vào hàng đợi
    
    Args:
        orders: Danh sách đơn hàng
        delay: Độ trễ giữa các lần gửi (giây)
    """
    global channel
    
    if channel is None:
        init_channel()
    
    print("\n" + "="*70)
    print(f"📤 GỬIA {len(orders)} ĐƠN HÀNG VÀO RABBITMQ")
    print("="*70 + "\n")
    
    for i, order in enumerate(orders, 1):
        try:
            channel.basic_publish(
                exchange="",
                routing_key="order_queue",
                body=json.dumps(order),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent message
                    content_type='application/json'
                )
            )
            
            print(
                f"[{i:2d}/{len(orders)}] ✅ Đơn #{order['id']:<3} | "
                f"{order['customer']:<15} | "
                f"{order['product']['name']:<20} | "
                f"Thời gian: {order['process_time']}s"
            )
            
            time.sleep(delay)
            
        except Exception as e:
            print(
                f"[{i:2d}/{len(orders)}] ❌ Lỗi: {str(e)}"
            )
    
    print("\n" + "="*70)
    print(f"✅ Tất cả {len(orders)} đơn hàng đã được gửi!")
    print("="*70 + "\n")


# =========================
# Get Queue Status
# =========================
def get_queue_stats():
    """Lấy thống kê hàng đợi"""
    global channel
    
    if channel is None:
        init_channel()
    
    try:
        method = channel.queue_declare(
            queue="order_queue",
            passive=True
        )
        
        message_count = method.method.message_count
        consumer_count = method.method.consumer_count
        
        print("\n📊 THỐNG KÊ HÀNG ĐỢI:")
        print(f"   📦 Số đơn chưa xử lý: {message_count}")
        print(f"   👷 Số worker đang kết nối: {consumer_count}\n")
        
        return {
            "message_count": message_count,
            "consumer_count": consumer_count
        }
        
    except Exception as e:
        print(f"❌ Lỗi lấy thống kê: {str(e)}")
        return None


# =========================
# Clear Queue
# =========================
def purge_queue():
    """Xóa tất cả đơn hàng trong hàng đợi"""
    global channel
    
    if channel is None:
        init_channel()
    
    try:
        channel.queue_purge("order_queue")
        print("✅ Hàng đợi đã được làm trống\n")
    except Exception as e:
        print(f"❌ Lỗi xóa hàng đợi: {str(e)}")


if __name__ == "__main__":
    # Test publish single order
    init_channel()
    
    test_order = {
        "id": 1,
        "customer": "Test Customer",
        "product": {
            "id": 1,
            "name": "Test Product"
        },
        "quantity": 1,
        "process_time": 3,
        "status": "Pending",
        "created_at": datetime.now().isoformat()
    }
    
    publish_order(test_order)
    
    stats = get_queue_stats()
