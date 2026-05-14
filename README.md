# 🛍️ SHOPEE MINI - Hệ Thống Xử Lý Đơn Hàng

Một hệ thống quản lý đơn hàng hoàn chỉnh sử dụng **RabbitMQ** (Message Queue), **Redis** (Pub/Sub), **SQLite** (Database), và **FastAPI** (REST API).

## 📋 Mục Lục

1. [Tính Năng](#tính-năng)
2. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
3. [Cài Đặt](#cài-đặt)
4. [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
5. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
6. [API Documentation](#api-documentation)
7. [Ví Dụ Chạy](#ví-dụ-chạy)
8. [Cách Thức Hoạt Động](#cách-thức-hoạt-động)

---

## ✨ Tính Năng

### 🎯 Yêu Cầu Cơ Bản
- ✅ **Tạo 10-20 đơn hàng** với thông tin ngẫu nhiên
- ✅ **Gửi đơn hàng vào RabbitMQ** để xử lý
- ✅ **Tạo 3+ worker** xử lý đơn hàng song song
- ✅ **Thông báo real-time** qua Redis Pub/Sub
- ✅ **Logging chi tiết** với timestamps

### 🚀 Yêu Cầu Nâng Cao
- ✅ **Số lượng worker động** (nhập khi chạy)
- ✅ **Thống kê hiệu suất** an toàn với Thread Lock
- ✅ **Retry logic** khi xử lý lỗi
- ✅ **Trạng thái đơn hàng**: Pending → Processing → Completed/Failed
- ✅ **Ghi log thời gian**: bắt đầu, kết thúc, thời gian tổng
- ✅ **FastAPI** cho REST API quản lý

### 🔧 Mở Rộng
- ✅ Lưu lịch sử đơn hàng vào SQLite
- ✅ Dashboard web (tùy chọn)
- ✅ Gửi email thông báo (tùy chọn)
- ✅ Analytics & reporting

---

## 🖥️ Yêu Cầu Hệ Thống

- Python 3.8+
- Docker & Docker Compose
- RabbitMQ 3.x
- Redis 6.x+

---

## 📦 Cài Đặt

### 1️⃣ Clone/Setup Repository

```bash
cd c:\Users\fpt\shopee_mini
```

### 2️⃣ Tạo Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Khởi Động RabbitMQ & Redis

```bash
docker-compose up -d
```

**Kiểm tra trạng thái:**
```bash
docker-compose ps

# Output:
# CONTAINER ID   IMAGE              STATUS
# xxx            rabbitmq:3-management   Up
# yyy            redis:latest       Up
```

**RabbitMQ Management UI:** http://localhost:15672
- Username: `guest`
- Password: `guest`

---

## 📁 Cấu Trúc Dự Án

```
shopee_mini/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── database.py                # SQLite config
│   ├── models.py                  # Order & Product models
│   ├── schemas.py                 # Pydantic schemas
│   ├── producer.py                # Gửi đơn hàng vào RabbitMQ
│   ├── worker.py                  # Single worker
│   ├── subscriber.py              # Lắng nghe Redis notifications
│   ├── multi_worker.py            # Multiple workers (recommended)
│   ├── order_generator.py         # Tạo đơn hàng mẫu
│   ├── performance_analyzer.py    # Phân tích hiệu suất
│   └── services/
│       ├── order_service.py
│       └── product_service.py
├── run_producer.py                # Chạy producer
├── run_multi_worker.py            # Chạy multiple workers
├── run_subscriber.py              # Chạy subscriber
├── run_demo.py                    # Menu demo
├── docker-compose.yml             # RabbitMQ + Redis
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 📌 Quy Trình Chạy Hệ Thống

**Terminal 1: Producer** (Tạo & gửi đơn)
```bash
python run_producer.py
# Nhập: 15 (số lượng đơn)
# Kết quả: 15 đơn được gửi vào RabbitMQ
```

**Terminal 2: Multi-Worker** (Xử lý đơn)
```bash
python run_multi_worker.py
# Nhập: 3 (số lượng nhân viên)
# Kết quả: 3 worker bắt đầu xử lý từ hàng đợi
```

**Terminal 3: Subscriber** (Lắng nghe thông báo)
```bash
python run_subscriber.py
# Hiển thị: Thông báo khi đơn hoàn thành
```

### 📊 Xem Thống Kê

Khi nhấn `Ctrl+C` ở các Terminal, hệ thống sẽ in:
- ✅ Số đơn mỗi worker xử lý
- ⏱️ Tổng thời gian xử lý
- ❌ Số lỗi & retry
- 📈 Thời gian trung bình/đơn

---

## 📡 API Documentation

### ✅ Base URL
```
http://localhost:8000
```

### 🏥 Health Check

**GET** `/`
```json
{
  "message": "Shopee Mini API is running ✅",
  "version": "1.0.0",
  "timestamp": "2024-05-14T10:30:00.000000"
}
```

### 📦 Products

**GET** `/products`
```json
{
  "total": 5,
  "products": [
    {"id": 1, "name": "iPhone 16", "stock": 10, "price": 30000000},
    {"id": 2, "name": "MacBook Pro", "stock": 5, "price": 55000000}
  ]
}
```

**GET** `/products/{id}`
```json
{
  "id": 1,
  "name": "iPhone 16",
  "stock": 10,
  "price": 30000000
}
```

### 🛒 Orders

**POST** `/orders`
```json
{
  "customer": "Nguyễn Văn A",
  "product_id": 1,
  "quantity": 2
}
```

Response:
```json
{
  "message": "Order created and sent to queue ✅",
  "order_id": 1,
  "status": "Pending",
  "customer": "Nguyễn Văn A"
}
```

**GET** `/orders`
```json
{
  "total": 15,
  "orders": [...]
}
```

**GET** `/orders/{id}`
```json
{
  "id": 1,
  "customer": "Nguyễn Văn A",
  "product_id": 1,
  "quantity": 2,
  "status": "Completed"
}
```

**PATCH** `/orders/{id}/status`
```json
{
  "message": "Order status updated ✅",
  "order_id": 1,
  "status": "Completed"
}
```

### 📊 Queue & System

**GET** `/queue/status`
```json
{
  "queue_name": "order_queue",
  "messages_pending": 5,
  "active_consumers": 3,
  "timestamp": "2024-05-14T10:30:00.000000"
}
```

**POST** `/queue/clear`
```json
{
  "message": "Queue cleared ✅",
  "timestamp": "2024-05-14T10:30:00.000000"
}
```

**GET** `/system/info`
```json
{
  "system": "Shopee Mini Order Management System",
  "version": "1.0.0",
  "database": {
    "total_orders": 50,
    "completed": 48,
    "pending": 2
  },
  "timestamp": "2024-05-14T10:30:00.000000"
}
```

---

## 💡 Ví Dụ Chạy

### Ví Dụ 1: Chạy Từ Menu

```bash
python run_demo.py

# Output:
# ======================================================================
# 🎯 MENU HỆ THỐNG XỬ LÝ ĐƠN HÀNG
# ======================================================================
# 
# 1️⃣  Xem hướng dẫn sử dụng
# 2️⃣  Khởi động Producer (gửi đơn)
# 3️⃣  Khởi động Multi-Worker (xử lý đơn)
# 4️⃣  Khởi động Subscriber (lắng nghe)
# 5️⃣  Tạo đơn hàng mẫu
# 0️⃣  Thoát
# 
# Chọn (0-5): 1
```

### Ví Dụ 2: Chạy Producer

```bash
python run_producer.py

# Output:
# ======================================================================
# 📤 PRODUCER - TẠO VÀ GỬI ĐƠN HÀNG
# ======================================================================
# 
# ❓ Xóa các đơn hàng cũ trong hàng đợi? (y/n): y
# ✅ Hàng đợi đã được làm trống
# 
# 📌 Nhập số lượng đơn (10-20, default 15): 15
# ⏳ Tạo 15 đơn hàng...
# 
# ============================================================
# 📋 DANH SÁCH 15 ĐƠN HÀNG
# ============================================================
# 
#  Đơn #1   | Nguyễn Văn A   | iPhone 16            | SL: 2 | Thời gian: 3s
#  Đơn #2   | Trần Thị B     | MacBook Pro M4       | SL: 1 | Thời gian: 5s
# ...
```

### Ví Dụ 3: Chạy Multi-Worker

```bash
python run_multi_worker.py

# Output:
# ======================================================================
# 🚀 HỆ THỐNG XỬ LÝ ĐƠN HÀNG VỚI RABBITMQ & REDIS
# ======================================================================
# 
# 📌 Nhập số lượng nhân viên (1-10): 3
# 🏢 Khởi động 3 nhân viên...
# 
# [10:30:01] ℹ️  [Nhân viên #1] Khởi động worker
# [10:30:01] ℹ️  [Nhân viên #2] Khởi động worker
# [10:30:01] ℹ️  [Nhân viên #3] Khởi động worker
# [10:30:02] ⏳ [Nhân viên #1] Đang xử lý đơn #1 | Khách: Nguyễn Văn A...
# [10:30:02] ⏳ [Nhân viên #2] Đang xử lý đơn #2 | Khách: Trần Thị B...
# [10:30:05] ✅ [Nhân viên #1] ✨ Hoàn thành đơn #1 trong 3.0s
```

---

## 🔧 Cách Thức Hoạt Động

### Luồng Xử Lý

```
┌─────────────────┐
│  Producer       │  (Tạo 15 đơn)
└────────┬────────┘
         │
         v
┌─────────────────────────────────────┐
│  RabbitMQ (order_queue)             │  (Hàng đợi 15 đơn)
│  [order #1] [order #2] ... [#15]    │
└────────┬────────────────────────────┘
         │
    ┌────┴────┬───────┐
    v         v       v
┌───────┐ ┌──────┐ ┌──────┐
│Worker1│ │Worker2│ │Worker3│  (Xử lý song song)
└───┬───┘ └───┬──┘ └──┬───┘
    │         │       │
    └────┬────┴───┬───┘
         │        │
         v        v
┌─────────────────────────────────────┐
│  Redis Pub/Sub (order_channel)      │  (Thông báo)
│  "Đơn #1 hoàn thành"                │
└─────────────────────────────────────┘
         │
         v
┌─────────────────┐
│  Subscriber     │  (Lắng nghe & in thông báo)
└─────────────────┘
```

### Chi Tiết Từng Bước

1. **Producer** đọc 15 đơn hàng từ `order_generator`
2. Gửi từng đơn vào RabbitMQ `order_queue`
3. **Worker 1, 2, 3** cùng lúc lấy đơn từ queue
4. Mỗi worker xử lý (chờ 1-5 giây)
5. Hoàn thành → Publish thông báo qua **Redis Pub/Sub**
6. **Subscriber** nhận thông báo → In ra màn hình
7. Lặp lại cho đến hết đơn trong queue

---

## 📊 Thống Kê & Monitoring

### Xem Thống Kê Tức Thời

```bash
# Terminal riêng
curl http://localhost:8000/queue/status

# Output:
# {
#   "queue_name": "order_queue",
#   "messages_pending": 12,
#   "active_consumers": 3,
#   "timestamp": "2024-05-14T10:30:00.000000"
# }
```

### Xem Thống Kê Cuối Cùng (khi Ctrl+C)

```
======================================================================
📊 THỐNG KÊ HIỆU SUẤT TỐT
======================================================================

👷 Nhân viên #1:
   ✅ Đơn xử lý: 5
   ⏱️  Tổng thời gian: 15.3s
   ⏰ Thời gian trung bình/đơn: 3.06s
   ❌ Đơn thất bại: 0
   🔄 Lần retry: 0

👷 Nhân viên #2:
   ✅ Đơn xử lý: 5
   ⏱️  Tổng thời gian: 18.2s
   ⏰ Thời gian trung bình/đơn: 3.64s
   ❌ Đơn thất bại: 0
   🔄 Lần retry: 1

...

======================================================================
```

---

## 🛠️ Troubleshooting

### ❌ Lỗi: "Connection refused"

**Nguyên nhân:** RabbitMQ hoặc Redis chưa chạy

**Giải pháp:**
```bash
docker-compose up -d
docker-compose ps  # Kiểm tra trạng thái
```

### ❌ Lỗi: "ModuleNotFoundError: No module named 'pika'"

**Giải pháp:**
```bash
pip install -r requirements.txt
```

### ❌ Worker không nhận đơn

**Nguyên nhân:** RabbitMQ queue trống

**Giải pháp:**
```bash
python run_producer.py  # Gửi đơn trước
```

### ❌ Subscriber không nhận thông báo

**Giải pháp:**
```bash
# 1. Đảm bảo Redis chạy
docker-compose ps

# 2. Chạy subscriber trước worker
python run_subscriber.py

# 3. Sau đó chạy producer & multi-worker
```

---

## 📚 Tài Liệu Tham Khảo

- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Redis Documentation](https://redis.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

## 📝 License

MIT License

---

## 👨‍💻 Author

Shopee Mini Order Management System v1.0.0

**Viết bởi:** GitHub Copilot
**Ngày:** 2024-05-14

---

## 🎯 Tiếp Theo

Để mở rộng hệ thống:

1. **Thêm Authentication** - JWT tokens
2. **Thêm Database** - PostgreSQL thay SQLite
3. **Thêm Caching** - Redis caching
4. **Thêm Monitoring** - Prometheus + Grafana
5. **Thêm Logging** - ELK Stack
6. **Thêm Testing** - Pytest + Integration tests
7. **Deploy** - Docker, Kubernetes, AWS/Azure

---

**🚀 Hãy bắt đầu!**

```bash
python run_producer.py     # Terminal 1
python run_multi_worker.py # Terminal 2 (trong terminal mới)
python run_subscriber.py   # Terminal 3 (trong terminal mới)
```

Chúc bạn thành công! 🎉
