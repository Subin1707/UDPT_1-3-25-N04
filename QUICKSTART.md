# 🚀 QUICK START GUIDE

## Bước 1: Chuẩn Bị

```bash
# Vào thư mục project
cd c:\Users\fpt\shopee_mini

# Kích hoạt virtual environment
.venv\Scripts\activate

# Kiểm tra dependencies
pip list | grep -E "pika|redis"
```

## Bước 2: Khởi Động RabbitMQ & Redis

```bash
# Chạy docker-compose (nếu chưa chạy)
docker-compose up -d

# Kiểm tra trạng thái
docker-compose ps

# Output:
# CONTAINER    IMAGE              STATUS
# shopee_rabbitmq   rabbitmq:3     Up
# shopee_redis      redis:latest   Up
```

**RabbitMQ Management:** http://localhost:15672 (guest/guest)

## Bước 3: Chạy System (3 Terminal)

### Terminal 1: Producer (Gửi Đơn)

```bash
cd c:\Users\fpt\shopee_mini
.venv\Scripts\activate
python run_producer.py

# Khi được hỏi:
# Xóa đơn cũ? (y/n): y
# Số lượng đơn (10-20): 15
```

### Terminal 2: Multi-Worker (Xử Lý Đơn)

```bash
cd c:\Users\fpt\shopee_mini
.venv\Scripts\activate
python run_multi_worker.py

# Khi được hỏi:
# Số lượng nhân viên (1-10): 3
```

### Terminal 3: Subscriber (Lắng Nghe)

```bash
cd c:\Users\fpt\shopee_mini
.venv\Scripts\activate
python run_subscriber.py

# Output: Lắng nghe thông báo từ Redis
```

## Kết Quả

Bạn sẽ thấy:

```
Terminal 1 (Producer):
✅ Đơn #1 | Nguyễn Văn A | iPhone 16 | SL: 2 | Thời gian: 3s
✅ Đơn #2 | Trần Thị B | MacBook Pro M4 | SL: 1 | Thời gian: 5s
...

Terminal 2 (Worker):
⏳ [Nhân viên #1] Đang xử lý đơn #1 | Khách: Nguyễn...
⏳ [Nhân viên #2] Đang xử lý đơn #2 | Khách: Trần...
✅ [Nhân viên #1] ✨ Hoàn thành đơn #1 trong 3.0s
✅ [Nhân viên #2] ✨ Hoàn thành đơn #2 trong 5.1s
...

Terminal 3 (Subscriber):
🎉 ĐƠN HÀNG #1 ĐÃ HOÀN THÀNH!
👷 Xử lý bởi: Nhân viên #1
⏱️ Thời gian xử lý: 3.0s
✅ Trạng thái: Completed
...
```

## Xem Thống Kê (Khi Hoàn Thành)

Nhấn `Ctrl+C` ở Terminal 2 để xem:

```
📊 THỐNG KÊ HIỆU SUẤT TỐT
==================

👷 Nhân viên #1:
   ✅ Đơn xử lý: 5
   ⏱️ Tổng thời gian: 15.3s
   ...
```

## Kiểm Tra Qua API

```bash
# Lấy danh sách đơn
curl http://localhost:8000/orders

# Lấy thống kê hàng đợi
curl http://localhost:8000/queue/status

# Lấy thông tin hệ thống
curl http://localhost:8000/system/info
```

## 📂 File Chính

- `run_producer.py` - Gửi đơn
- `run_multi_worker.py` - Xử lý đơn
- `run_subscriber.py` - Lắng nghe
- `run_demo.py` - Menu tương tác
- `README.md` - Tài liệu đầy đủ
- `IMPLEMENTATION.md` - Chi tiết triển khai

## 🎯 Ý Nghĩa Các Icon

- ✅ Thành công
- ❌ Lỗi
- ⏳ Đang xử lý
- 🎉 Hoàn thành
- ⏱️ Thời gian
- 📊 Thống kê
- 👷 Worker
- 📦 Đơn hàng

## Cách Dừng

- **Ctrl+C** - Dừng từng component
- **docker-compose down** - Tắt RabbitMQ & Redis

---

**Chúc bạn chạy thành công! 🚀**
