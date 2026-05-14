"""
Run Multi-Worker - Khởi động nhiều worker xử lý đơn hàng
"""
import sys

sys.path.insert(0, '/app')

from app.multi_worker import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Dừng tất cả worker")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
