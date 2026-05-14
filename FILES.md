# 📁 File Structure & Purpose

## Tổng Quan Hệ Thống

```
shopee_mini/
├── 📄 Configuration Files
│   ├── docker-compose.yml          # RabbitMQ + Redis setup
│   ├── requirements.txt            # Python dependencies
│   └── .gitignore                  # Git ignore rules
│
├── 📚 Documentation
│   ├── README.md                   # Complete documentation (Vietnamese)
│   ├── QUICKSTART.md               # Quick start guide
│   └── IMPLEMENTATION.md           # Implementation details
│
├── 🚀 Runner Scripts (Main Entry Points)
│   ├── run_demo.py                 # Interactive menu
│   ├── run_producer.py             # Send orders to queue
│   ├── run_multi_worker.py         # Process orders (multi-threaded)
│   └── run_subscriber.py           # Listen for notifications
│
└── 📦 Application Code (app/)
    ├── __init__.py
    │
    ├── 🔌 Core Components
    │   ├── main.py                 # FastAPI application & endpoints
    │   ├── database.py             # SQLite configuration
    │   ├── producer.py             # RabbitMQ producer (batch & single)
    │   ├── worker.py               # Single worker (older version)
    │   ├── subscriber.py           # Redis Pub/Sub listener
    │   └── multi_worker.py         # Multi-threaded workers (RECOMMENDED)
    │
    ├── 📊 Data Models
    │   ├── models.py               # SQLAlchemy models (Order, Product)
    │   └── schemas.py              # Pydantic schemas
    │
    ├── 🛠️ Analysis & Tracking
    │   ├── order_generator.py      # Generate sample orders
    │   └── performance_analyzer.py # Track performance metrics
    │
    └── 🎯 Services
        └── services/
            ├── order_service.py    # Order business logic
            └── product_service.py  # Product management
```

---

## 📄 File Details

### 🚀 Runner Scripts (Chạy Trực Tiếp)

#### `run_demo.py`
- **Mục đích:** Menu tương tác cho người dùng
- **Chạy:** `python run_demo.py`
- **Tính năng:**
  - Menu 6 tùy chọn
  - Hướng dẫn sử dụng
  - Khởi động components
  - Tạo đơn hàng mẫu
- **Khi dùng:** Lần đầu tiên hoặc đơn giản

#### `run_producer.py`
- **Mục đích:** Tạo & gửi đơn hàng vào RabbitMQ
- **Chạy:** `python run_producer.py`
- **Tính năng:**
  - Hỏi có xóa hàng đợi cũ
  - Nhập số lượng đơn (10-20)
  - Tạo đơn hàng ngẫu nhiên
  - Gửi batch vào queue
  - Hiển thị thống kê queue
- **Khi dùng:** Lần đầu hoặc khi muốn tạo đơn mới

#### `run_multi_worker.py`
- **Mục đích:** Khởi động nhiều worker xử lý đơn
- **Chạy:** `python run_multi_worker.py`
- **Tính năng:**
  - Hỏi số lượng worker (1-10)
  - Tạo thread cho mỗi worker
  - Xử lý đơn song song
  - Thread-safe statistics
  - Retry logic
  - In thống kê khi Ctrl+C
- **Khi dùng:** Xử lý đơn hàng

#### `run_subscriber.py`
- **Mục đích:** Lắng nghe thông báo từ Redis
- **Chạy:** `python run_subscriber.py`
- **Tính năng:**
  - Kết nối Redis Pub/Sub
  - Lắng nghe order_channel
  - Hiển thị thông báo hoàn thành
  - Theo dõi thống kê
  - In tóm tắt khi Ctrl+C
- **Khi dùng:** Cùng lúc với worker

---

### 🔌 Core Application Files

#### `app/main.py`
- **Mục đích:** FastAPI application chính
- **Tính năng:**
  - 20+ API endpoints
  - Health check
  - Product management
  - Order management
  - Queue status
  - System info
- **Endpoints:** `/`, `/products`, `/orders`, `/queue/status`, `/system/info`

#### `app/database.py`
- **Mục đích:** Cấu hình SQLite database
- **Tính năng:**
  - SQLAlchemy engine
  - Session factory
  - Base model class
  - Dependency injection
- **Database:** `sqlite:///./shop.db`

#### `app/producer.py`
- **Mục đích:** Gửi đơn hàng vào RabbitMQ
- **Tính năng:**
  - Gửi đơn đơn lẻ
  - Gửi batch đơn
  - Persistent messages
  - Queue stats
  - Queue purge
  - Chi tiết logging
- **Queue:** `order_queue` (durable)

#### `app/multi_worker.py` ⭐ RECOMMENDED
- **Mục đích:** Xử lý đơn hàng từ queue (multi-threaded)
- **Tính năng:**
  - Thread-safe statistics
  - Dynamic worker count (1-10)
  - Retry logic (max 3 lần)
  - Error handling
  - Redis notifications
  - Detailed logging
  - Worker pool management
- **Class:** `WorkerStats` (Lock-based)

#### `app/worker.py`
- **Mục đích:** Single worker (legacy)
- **Tính năng:**
  - Đơn worker thread
  - Redis pub/sub
  - Basic logging
- **Note:** Dùng `multi_worker.py` thay vào

#### `app/subscriber.py`
- **Mục đích:** Lắng nghe thông báo hoàn thành
- **Tính náng:**
  - Redis Pub/Sub listener
  - Real-time notifications
  - Statistics tracking
  - Summary on exit
- **Channel:** `order_channel`

#### `app/models.py`
- **Mục đích:** SQLAlchemy ORM models
- **Models:**
  - `Product` - Sản phẩm
  - `Order` - Đơn hàng
- **Fields:** ID, name, customer, status, etc.

#### `app/schemas.py`
- **Mục đích:** Pydantic validation schemas
- **Schemas:**
  - `ProductBase`, `ProductResponse`
  - `OrderCreate`, `OrderResponse`
- **Validation:** Input validation & response serialization

---

### 🛠️ Utility & Analysis Files

#### `app/order_generator.py`
- **Mục đích:** Tạo đơn hàng mẫu ngẫu nhiên
- **Tính năng:**
  - Tạo 10-20 đơn
  - Ngẫu nhiên: khách, sản phẩm, SL, thời gian
  - In danh sách đẹp
- **Hàm chính:** `generate_orders(num)`, `print_orders(orders)`

#### `app/performance_analyzer.py`
- **Mục đích:** Theo dõi & phân tích hiệu suất
- **Classes:**
  - `PerformanceTracker` - Tracking metrics
  - `PerformanceLogger` - Log to file
- **Metrics:** orders/worker, time, throughput, etc.

---

### 📊 Service Layer

#### `app/services/order_service.py`
- **Mục đích:** Business logic cho đơn hàng
- **Hàm:**
  - `create_order()` - Tạo order
  - `get_all_orders()` - Lấy tất cả
  - `get_order_by_id()` - Lấy chi tiết
  - `update_order_status()` - Cập nhật trạng thái

#### `app/services/product_service.py`
- **Mục đích:** Business logic cho sản phẩm
- **Hàm:**
  - `seed_products()` - Tạo sản phẩm mẫu
  - `get_all_products()` - Lấy tất cả
  - `get_product_by_id()` - Lấy chi tiết
  - `create_product()` - Tạo sản phẩm

---

### 📚 Documentation Files

#### `README.md` (Tài Liệu Chính)
- Tính năng đầy đủ
- Cài đặt step-by-step
- Cấu trúc dự án
- API documentation
- Ví dụ chạy
- Troubleshooting
- Giải thích cách hoạt động

#### `QUICKSTART.md` (Hướng Dẫn Nhanh)
- Bước chuẩn bị
- Khởi động RabbitMQ & Redis
- Chạy 3 terminals
- Xem kết quả
- Kiểm tra qua API

#### `IMPLEMENTATION.md` (Chi Tiết Triển Khai)
- Hoàn thành tất cả yêu cầu
- Chi tiết từng tính năng
- Ví dụ code
- Kiến trúc hệ thống
- Metrics tracked
- Điểm nổi bật

#### This File: `FILES.md`
- Danh sách tất cả files
- Mục đích mỗi file
- Tính năng chính
- Khi nào dùng

---

## 🚀 Cách Sử Dụng

### Lần Đầu Tiên (Easy Way)
```bash
python run_demo.py
# Chọn từ menu
```

### Lần Thường Xuyên (Recommended Way)
```bash
# Terminal 1
python run_producer.py

# Terminal 2 (mở terminal mới)
python run_multi_worker.py

# Terminal 3 (mở terminal mới)
python run_subscriber.py
```

### Advanced: Sử Dụng FastAPI
```bash
uvicorn app.main:app --reload
# Truy cập: http://localhost:8000/docs
```

---

## 📊 Data Flow

```
run_producer.py
    ↓
app/order_generator.py → Tạo 15 đơn
    ↓
app/producer.py → Gửi vào RabbitMQ
    ↓
            ┌──────────────────┐
            │   RabbitMQ       │
            │  order_queue     │
            └────────┬─────────┘
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    Worker 1    Worker 2     Worker 3
    (multi_worker.py)
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
            ┌──────────────────┐
            │   Redis Pub/Sub   │
            │  order_channel    │
            └────────┬─────────┘
                     ↓
            run_subscriber.py
            (Hiển thị thông báo)
```

---

## 🎯 Dependency Graph

```
run_producer.py
    ├── app.order_generator
    ├── app.producer
    └── app.models → app.database

run_multi_worker.py
    └── app.multi_worker
        ├── pika (RabbitMQ)
        ├── redis
        └── threading

run_subscriber.py
    └── app.subscriber
        ├── redis
        └── json

app/main.py
    ├── app.models
    ├── app.database
    ├── app.schemas
    ├── app.producer
    └── app.services
        ├── order_service
        └── product_service
```

---

## 📦 Dependencies (requirements.txt)

```
fastapi              # Web framework
uvicorn             # ASGI server
sqlalchemy          # ORM
pydantic            # Validation
pika                # RabbitMQ client
redis               # Redis client
python-multipart    # Form data support
```

---

## 💾 Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    stock INTEGER DEFAULT 0,
    price INTEGER DEFAULT 0
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer VARCHAR NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status VARCHAR DEFAULT 'Pending'
);
```

---

## 🔄 Config Files

### `docker-compose.yml`
- RabbitMQ (port 5672, admin 15672)
- Redis (port 6379)
- FastAPI (port 8000)

### `requirements.txt`
- Python packages needed
- Version specifications

---

## ✅ Checklist

- ✅ Producer - Gửi đơn
- ✅ Multi-Worker - Xử lý đơn
- ✅ Subscriber - Lắng nghe
- ✅ API - REST endpoints
- ✅ Database - SQLite
- ✅ Logging - Timestamps
- ✅ Statistics - Thread-safe
- ✅ Retry Logic - Error handling
- ✅ Documentation - Complete
- ✅ Runnable - Ready to use

---

**Tất cả files đều sẵn sàng để chạy! 🚀**
