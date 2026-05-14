"""
Order Subscriber - Lắng nghe thông báo đơn hàng từ Redis Pub/Sub
Hiển thị thông báo khi đơn hàng hoàn thành
"""
import redis
import json
from datetime import datetime
from collections import defaultdict

# =========================
# Statistics Tracking
# =========================
class SubscriberStats:
    """Thống kê thông báo nhận được"""
    def __init__(self):
        self.completed_orders = []
        self.worker_completions = defaultdict(int)
        self.total_processing_time = 0
    
    def add_completion(self, order_data: dict):
        """Thêm thông báo hoàn thành"""
        self.completed_orders.append(order_data)
        self.worker_completions[order_data.get("worker", "Unknown")] += 1
        
        # Tính tổng thời gian từ duration string
        duration_str = order_data.get("duration", "0s")
        try:
            duration = float(duration_str.replace("s", ""))
            self.total_processing_time += duration
        except:
            pass
    
    def print_summary(self):
        """In tóm tắt"""
        print("\n" + "="*70)
        print("📊 THỐNG KÊ HOÀN THÀNH ĐƠN HÀNG")
        print("="*70)
        print(f"\n✅ Tổng đơn hoàn thành: {len(self.completed_orders)}")
        print(f"⏱️  Tổng thời gian xử lý: {self.total_processing_time:.1f}s")
        print(f"⏰ Thời gian trung bình: "
              f"{self.total_processing_time/len(self.completed_orders):.2f}s" 
              if self.completed_orders else "N/A")
        
        print("\n📈 Đơn hoàn thành theo nhân viên:")
        for worker, count in sorted(
            self.worker_completions.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(f"   • {worker}: {count} đơn")
        
        print("\n" + "="*70 + "\n")

# Global stats
subscriber_stats = SubscriberStats()

# =========================
# Redis Connection
# =========================
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# =========================
# Subscribe Channel
# =========================
pubsub = redis_client.pubsub()

pubsub.subscribe("order_channel")

print("\n" + "="*70)
print("📡 HỆ THỐNG LẮNG NGHE THÔNG BÁO ĐƠN HÀNG")
print("="*70)
print("⏳ Chờ thông báo từ Redis Pub/Sub...\n")

# =========================
# Listen Notifications
# =========================
try:
    for message in pubsub.listen():

        # Bỏ qua subscribe event
        if message["type"] != "message":
            continue

        data = json.loads(
            message["data"]
        )

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )
        
        # Thêm vào thống kê
        subscriber_stats.add_completion(data)

        order_id = data.get("order_id", "?")
        worker = data.get("worker", "Unknown")
        duration = data.get("duration", "?")
        status = data.get("status", "?")

        print("="*70)

        print(
            f"[{current_time}] 🎉 ĐƠN HÀNG #{order_id} "
            f"ĐÃ HOÀN THÀNH!"
        )

        print(
            f"👷 Xử lý bởi: {worker}"
        )
        
        print(
            f"⏱️  Thời gian xử lý: {duration}"
        )
        
        print(
            f"✅ Trạng thái: {status}"
        )

        print("="*70 + "\n")

except KeyboardInterrupt:
    print("\n\n🛑 Dừng lắng nghe")
    subscriber_stats.print_summary()
    exit(0)