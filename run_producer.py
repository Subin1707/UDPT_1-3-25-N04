"""
Run Producer - Tạo và gửi đơn hàng
"""
import sys
from datetime import datetime

sys.path.insert(0, '/app')

from app.order_generator import generate_orders, print_orders
from app.producer import publish_orders_batch, get_queue_stats, purge_queue

def main():
    print("\n" + "="*70)
    print("📤 PRODUCER - TẠO VÀ GỬI ĐƠN HÀNG")
    print("="*70)
    
    # Hỏi có xóa hàng đợi cũ không
    response = input("\n❓ Xóa các đơn hàng cũ trong hàng đợi? (y/n): ").lower()
    if response == 'y':
        purge_queue()
    
    # Hỏi số lượng đơn
    while True:
        try:
            num_orders = input("\n📌 Nhập số lượng đơn (10-20, default 15): ").strip()
            num_orders = int(num_orders) if num_orders else 15
            if 10 <= num_orders <= 20:
                break
            else:
                print("❌ Vui lòng nhập số từ 10 đến 20")
        except ValueError:
            print("❌ Vui lòng nhập một số nguyên")
    
    # Tạo đơn hàng
    print(f"\n⏳ Tạo {num_orders} đơn hàng...")
    orders = generate_orders(num_orders)
    
    # In danh sách đơn
    print_orders(orders)
    
    # Gửi đơn hàng
    print("\n⏳ Gửi đơn hàng vào RabbitMQ...")
    publish_orders_batch(orders, delay=0.3)
    
    # Lấy thống kê
    stats = get_queue_stats()
    
    if stats and stats['message_count'] > 0:
        print("✅ Các đơn hàng đã sẵn sàng cho worker xử lý!")
        print("\n💡 Bước tiếp theo:")
        print("   1. Mở terminal mới")
        print("   2. Chạy: python run_multi_worker.py")
        print("   3. Nhập số lượng nhân viên\n")
    
    input("\nNhấn Enter để thoát...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Dừng producer")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
