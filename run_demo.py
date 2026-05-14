"""
DEMO: Hệ thống xử lý đơn hàng với RabbitMQ & Redis
This is the main entry point to run the complete order management system
"""
import sys
import subprocess
import time
from datetime import datetime

# Add app to path
sys.path.insert(0, '/app')

def print_header(title):
    """In header"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70 + "\n")


def print_instructions():
    """In hướng dẫn sử dụng"""
    print_header("HƯỚNG DẪN SỬ DỤNG HỆ THỐNG XỬ LÝ ĐƠN HÀNG")
    
    instructions = """
📌 BƯỚC 1: Khởi động RabbitMQ và Redis
   • Chạy: docker-compose up -d
   • Kiểm tra: docker-compose ps

📌 BƯỚC 2: Tạo đơn hàng mẫu
   • Chạy: python -m app.order_generator
   • Tạo 10-20 đơn hàng ngẫu nhiên

📌 BƯỚC 3: Gửi đơn hàng vào hệ thống (Terminal 1)
   • Chạy: python run_producer.py
   • Sẽ gửi tất cả đơn hàng vào RabbitMQ

📌 BƯỚC 4: Khởi động các nhân viên xử lý (Terminal 2)
   • Chạy: python run_multi_worker.py
   • Nhập số lượng nhân viên (1-10)
   • Worker sẽ xử lý đơn hàng song song

📌 BƯỚC 5: Lắng nghe thông báo (Terminal 3)
   • Chạy: python run_subscriber.py
   • Sẽ hiển thị thông báo khi đơn hoàn thành

📌 BƯỚC 6: Xem thống kê (khi Ctrl+C các terminal)
   • Sẽ in ra:
     - Hiệu suất từng nhân viên
     - Tổng thời gian xử lý
     - Lỗi và retry

🎨 TÍNH NĂNG:
   ✅ Gửi 10-20 đơn hàng vào hàng đợi
   ✅ Nhiều worker xử lý song song (1-10 nhân viên)
   ✅ Retry logic khi xử lý lỗi
   ✅ Thông báo real-time qua Redis Pub/Sub
   ✅ Thống kê hiệu suất an toàn với Thread Lock
   ✅ Logging chi tiết với timestamp

📊 RabbitMQ Management: http://localhost:15672
   • User: guest
   • Password: guest
    """
    
    print(instructions)


def run_producer():
    """Chạy producer"""
    print_header("KHỞI ĐỘNG PRODUCER - GỬI ĐƠN HÀNG")
    
    print("Nhập lệnh sau trong terminal mới:\n")
    print("   python run_producer.py\n")
    print("hoặc chạy trực tiếp Python:\n")
    print("   from app.order_generator import generate_orders")
    print("   from app.producer import publish_orders_batch")
    print("   orders = generate_orders(15)")
    print("   publish_orders_batch(orders)\n")


def run_worker():
    """Chạy multi-worker"""
    print_header("KHỞI ĐỘNG MULTI-WORKER - XỬ LÝ ĐƠN HÀNG")
    
    print("Nhập lệnh sau trong terminal mới:\n")
    print("   python run_multi_worker.py\n")
    print("Sau đó nhập số lượng nhân viên (1-10)\n")


def run_subscriber():
    """Chạy subscriber"""
    print_header("KHỞI ĐỘNG SUBSCRIBER - LẮNG NGHE THÔNG BÁO")
    
    print("Nhập lệnh sau trong terminal mới:\n")
    print("   python run_subscriber.py\n")


def main_menu():
    """Menu chính"""
    print_header("MENU HỆ THỐNG XỬ LÝ ĐƠN HÀNG")
    
    menu = """
1️⃣  Xem hướng dẫn sử dụng
2️⃣  Khởi động Producer (gửi đơn)
3️⃣  Khởi động Multi-Worker (xử lý đơn)
4️⃣  Khởi động Subscriber (lắng nghe)
5️⃣  Tạo đơn hàng mẫu
0️⃣  Thoát

Chọn (0-5): """
    
    while True:
        try:
            choice = input(menu).strip()
            
            if choice == "1":
                print_instructions()
            
            elif choice == "2":
                run_producer()
            
            elif choice == "3":
                run_worker()
            
            elif choice == "4":
                run_subscriber()
            
            elif choice == "5":
                print_header("TẠO ĐƠN HÀNG MẪU")
                from app.order_generator import generate_orders, print_orders
                num = input("Nhập số lượng đơn (10-20, default 15): ").strip()
                try:
                    num = int(num) if num else 15
                    orders = generate_orders(num)
                    print_orders(orders)
                except ValueError:
                    orders = generate_orders(15)
                    print_orders(orders)
            
            elif choice == "0":
                print("\n👋 Tạm biệt!\n")
                break
            
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!\n")
            break
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🛍️  SHOPEE MINI - HỆ THỐNG XỬ LÝ ĐƠN HÀNG")
    print("="*70)
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        main_menu()
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
