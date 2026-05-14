"""
Multi-Worker Processor - Xử lý đơn hàng từ RabbitMQ
Hỗ trợ:
- Số lượng worker động (nhập khi chạy)
- Thống kê hiệu suất an toàn với thread lock
- Retry logic khi xử lý lỗi
- Logging chi tiết với timestamps
"""
import pika
import redis
import json
import time
import threading
import random
from datetime import datetime
from typing import Dict, Any
from collections import defaultdict

# =========================
# Global Statistics
# =========================
class WorkerStats:
    """Quản lý thống kê hiệu suất của worker"""
    def __init__(self):
        self.lock = threading.Lock()
        self.stats = defaultdict(lambda: {
            "orders_processed": 0,
            "total_time": 0,
            "failed_orders": 0,
            "retry_attempts": 0
        })
    
    def add_processed_order(self, worker_name: str, duration: float):
        """Thêm đơn hàng đã xử lý"""
        with self.lock:
            self.stats[worker_name]["orders_processed"] += 1
            self.stats[worker_name]["total_time"] += duration
    
    def add_failed_order(self, worker_name: str):
        """Thêm đơn hàng thất bại"""
        with self.lock:
            self.stats[worker_name]["failed_orders"] += 1
    
    def add_retry_attempt(self, worker_name: str):
        """Thêm lần retry"""
        with self.lock:
            self.stats[worker_name]["retry_attempts"] += 1
    
    def get_stats(self, worker_name: str) -> Dict:
        """Lấy thống kê của một worker"""
        with self.lock:
            return dict(self.stats[worker_name])
    
    def get_all_stats(self) -> Dict:
        """Lấy thống kê tất cả worker"""
        with self.lock:
            return dict(self.stats)
    
    def print_summary(self):
        """In tóm tắt thống kê"""
        with self.lock:
            print("\n" + "="*70)
            print("📊 THỐNG KÊ HIỆU SUẤT TỐT")
            print("="*70)
            
            total_orders = 0
            total_time = 0
            total_failed = 0
            
            for worker_name, stats in self.stats.items():
                processed = stats["orders_processed"]
                work_time = stats["total_time"]
                failed = stats["failed_orders"]
                retries = stats["retry_attempts"]
                
                total_orders += processed
                total_time += work_time
                total_failed += failed
                
                avg_time = work_time / processed if processed > 0 else 0
                
                print(f"\n👷 {worker_name}:")
                print(f"   ✅ Đơn xử lý: {processed}")
                print(f"   ⏱️  Tổng thời gian: {work_time:.1f}s")
                print(f"   ⏰ Thời gian trung bình/đơn: {avg_time:.2f}s")
                print(f"   ❌ Đơn thất bại: {failed}")
                print(f"   🔄 Lần retry: {retries}")
            
            print("\n" + "-"*70)
            print(f"📈 TỔNG CỘNG:")
            print(f"   ✅ Tổng đơn xử lý: {total_orders}")
            print(f"   ⏱️  Tổng thời gian: {total_time:.1f}s")
            print(f"   ❌ Tổng đơn thất bại: {total_failed}")
            print("="*70 + "\n")


# Global stats object
worker_stats = WorkerStats()

# =========================
# RabbitMQ & Redis Connection
# =========================
def create_rabbit_connection():
    """Tạo kết nối RabbitMQ"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue="order_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    return connection, channel

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# =========================
# Logger Function
# =========================
def log_message(worker_name: str, message: str, level: str = "INFO"):
    """Log tin nhắn với timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    level_icon = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️ ",
        "PROCESSING": "⏳"
    }.get(level, "")
    
    print(f"[{timestamp}] {level_icon} [{worker_name}] {message}")


# =========================
# Process Order Function
# =========================
def process_order(
    ch: Any,
    method: Any,
    properties: Any,
    body: bytes,
    worker_name: str,
    max_retries: int = 3
) -> bool:
    """
    Xử lý một đơn hàng
    
    Args:
        ch: RabbitMQ channel
        method: Delivery method
        properties: Message properties
        body: Message body
        worker_name: Tên worker
        max_retries: Số lần retry tối đa
    
    Returns:
        True nếu thành công, False nếu lỗi
    """
    order = json.loads(body)
    order_id = order["id"]
    start_time = datetime.now()
    
    log_message(
        worker_name,
        f"Đang xử lý đơn #{order_id} "
        f"| Khách: {order['customer']} "
        f"| Sản phẩm: {order['product']['name']}",
        "PROCESSING"
    )
    
    # Giả lập xử lý
    process_time = order.get("process_time", random.randint(1, 5))
    
    print(f"            → Thời gian xử lý dự tính: {process_time}s")
    
    # Retry logic - giả lập lỗi ngẫu nhiên
    retry_count = 0
    success = False
    
    while retry_count < max_retries and not success:
        try:
            # Giả lập xử lý có thể lỗi (10% chance)
            if random.random() < 0.1 and retry_count == 0:
                raise Exception("Lỗi xử lý tạm thời")
            
            time.sleep(process_time)
            success = True
            
        except Exception as e:
            retry_count += 1
            worker_stats.add_retry_attempt(worker_name)
            
            if retry_count < max_retries:
                log_message(
                    worker_name,
                    f"Lỗi xử lý đơn #{order_id}: {str(e)} "
                    f"(Retry {retry_count}/{max_retries})",
                    "WARNING"
                )
                time.sleep(1)  # Chờ trước khi retry
            else:
                log_message(
                    worker_name,
                    f"Đơn #{order_id} thất bại sau {max_retries} lần retry",
                    "ERROR"
                )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if success:
        order["status"] = "Completed"
        order["completed_at"] = end_time.isoformat()
        
        log_message(
            worker_name,
            f"✨ Hoàn thành đơn #{order_id} "
            f"trong {duration:.1f}s",
            "SUCCESS"
        )
        
        # Publish notification via Redis
        redis_client.publish(
            "order_channel",
            json.dumps({
                "order_id": order_id,
                "status": "Completed",
                "worker": worker_name,
                "duration": f"{duration:.1f}s",
                "completed_at": end_time.isoformat()
            })
        )
        
        # Update statistics
        worker_stats.add_processed_order(worker_name, duration)
        
        # 🆕 TẠO HÓA ĐƠN NGAY SAU KHI HOÀN THÀNH
        try:
            from app.database import SessionLocal
            from app.services.invoice_service import create_invoice, get_invoice_by_order_id
            from app.services.order_service import get_order_by_id
            from app.services.product_service import get_product_by_id
            
            db = SessionLocal()
            
            # Lấy thông tin order từ database
            db_order = get_order_by_id(db, order_id)
            
            if db_order:
                # Lấy thông tin sản phẩm
                product = get_product_by_id(db, db_order.product_id)
                
                if product:
                    # Kiểm tra xem đã có hóa đơn chưa
                    existing_invoice = get_invoice_by_order_id(db, order_id)
                    
                    if not existing_invoice:
                        # Tạo hóa đơn mới
                        invoice = create_invoice(
                            db=db,
                            order_id=order_id,
                            customer=db_order.customer,
                            product_name=product.name,
                            quantity=db_order.quantity,
                            unit_price=product.price
                        )
                        
                        log_message(
                            worker_name,
                            f"📄 Tạo hóa đơn #{invoice.invoice_number} "
                            f"cho đơn #{order_id} - Thành tiền: {invoice.total_amount:,.0f}₫",
                            "SUCCESS"
                        )
            
            db.close()
        except Exception as e:
            log_message(
                worker_name,
                f"⚠️  Lỗi tạo hóa đơn: {str(e)}",
                "WARNING"
            )
        
        # ACK message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        return True
    else:
        order["status"] = "Failed"
        worker_stats.add_failed_order(worker_name)
        
        # Nack and requeue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        return False


# =========================
# Worker Thread
# =========================
def worker_thread(
    worker_id: int,
    worker_name: str
):
    """
    Chạy một worker trong thread riêng
    
    Args:
        worker_id: ID của worker
        worker_name: Tên của worker
    """
    log_message(worker_name, "Khởi động worker", "INFO")
    
    try:
        connection, channel = create_rabbit_connection()
        
        def callback(ch, method, properties, body):
            process_order(ch, method, properties, body, worker_name)
        
        channel.basic_consume(
            queue="order_queue",
            on_message_callback=callback
        )
        
        log_message(
            worker_name,
            "Chờ đơn hàng từ hàng đợi...",
            "INFO"
        )
        
        channel.start_consuming()
        
    except KeyboardInterrupt:
        log_message(worker_name, "Dừng worker", "WARNING")
        connection.close()
    except Exception as e:
        log_message(worker_name, f"Lỗi: {str(e)}", "ERROR")


# =========================
# Main Function
# =========================
def main():
    """Chạy hệ thống với nhiều worker"""
    print("\n" + "="*70)
    print("🚀 HỆ THỐNG XỬ LÝ ĐƠN HÀNG VỚI RABBITMQ & REDIS")
    print("="*70)
    
    # Nhập số lượng worker
    while True:
        try:
            num_workers = int(
                input("\n📌 Nhập số lượng nhân viên (1-10): ")
            )
            if 1 <= num_workers <= 10:
                break
            else:
                print("❌ Vui lòng nhập số từ 1 đến 10")
        except ValueError:
            print("❌ Vui lòng nhập một số nguyên")
    
    # Tạo danh sách worker threads
    threads = []
    
    print(f"\n🏢 Khởi động {num_workers} nhân viên...\n")
    
    for i in range(num_workers):
        worker_name = f"Nhân viên #{i+1}"
        t = threading.Thread(
            target=worker_thread,
            args=(i+1, worker_name),
            daemon=True
        )
        threads.append(t)
        t.start()
        time.sleep(0.5)
    
    # Chờ tất cả threads
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n\n🛑 Dừng tất cả worker")
        
        # In thống kê trước khi thoát
        worker_stats.print_summary()
        exit(0)


if __name__ == "__main__":
    main()
