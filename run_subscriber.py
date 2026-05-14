"""
Run Subscriber - Lắng nghe thông báo đơn hàng từ Redis Pub/Sub
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    try:
        # Import subscriber module
        import app.subscriber
        # Subscriber code will run on import
    except KeyboardInterrupt:
        print("\n\n🛑 Dừng subscriber")
        exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
