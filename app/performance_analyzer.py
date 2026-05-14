"""
Performance Analyzer - Phân tích hiệu suất hệ thống
Theo dõi và hiển thị thống kê chi tiết về xử lý đơn hàng
"""
import json
import time
from datetime import datetime
from collections import defaultdict

class PerformanceTracker:
    """Theo dõi và phân tích hiệu suất"""
    
    def __init__(self):
        self.orders_data = []
        self.worker_data = defaultdict(list)
        self.timestamps = defaultdict(list)
    
    def add_order_record(self, order_id, worker, start_time, end_time, status, duration):
        """Thêm bản ghi xử lý đơn"""
        self.orders_data.append({
            "order_id": order_id,
            "worker": worker,
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "duration": duration
        })
        
        self.worker_data[worker].append(duration)
        self.timestamps[worker].append(end_time)
    
    def get_worker_stats(self, worker=None):
        """Lấy thống kê của worker"""
        if worker:
            durations = self.worker_data.get(worker, [])
        else:
            durations = [d for durations in self.worker_data.values() for d in durations]
        
        if not durations:
            return None
        
        total = sum(durations)
        count = len(durations)
        avg = total / count
        min_time = min(durations)
        max_time = max(durations)
        
        return {
            "count": count,
            "total": total,
            "average": avg,
            "min": min_time,
            "max": max_time
        }
    
    def get_throughput(self, worker, time_window=60):
        """Tính lưu lượng (orders/second)"""
        if worker not in self.timestamps:
            return 0
        
        current_time = time.time()
        recent_timestamps = [
            t for t in self.timestamps[worker]
            if current_time - t < time_window
        ]
        
        throughput = len(recent_timestamps) / time_window
        return throughput
    
    def print_full_report(self):
        """In báo cáo chi tiết"""
        print("\n" + "="*80)
        print("📊 BÁO CÁO PHÂN TÍCH HIỆU SUẤT CHI TIẾT")
        print("="*80)
        
        print(f"\n📈 TỔNG QUAN:")
        print(f"   • Tổng đơn xử lý: {len(self.orders_data)}")
        print(f"   • Tổng worker: {len(self.worker_data)}")
        print(f"   • Thời gian báo cáo: {datetime.now().isoformat()}")
        
        # Overall stats
        overall_stats = self.get_worker_stats()
        if overall_stats:
            print(f"\n⏱️  THỐNG KÊ THỜI GIAN TỔNG THỂ:")
            print(f"   • Thời gian xử lý trung bình: {overall_stats['average']:.2f}s")
            print(f"   • Thời gian nhanh nhất: {overall_stats['min']:.2f}s")
            print(f"   • Thời gian chậm nhất: {overall_stats['max']:.2f}s")
            print(f"   • Tổng thời gian: {overall_stats['total']:.1f}s")
        
        # Per-worker stats
        print(f"\n👷 THỐNG KÊ TỪNG NHÂN VIÊN:")
        
        workers_sorted = sorted(
            self.worker_data.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for worker, durations in workers_sorted:
            stats = self.get_worker_stats(worker)
            throughput = self.get_throughput(worker)
            
            print(f"\n   {worker}:")
            print(f"      ✅ Đơn xử lý: {stats['count']}")
            print(f"      ⏱️  Trung bình: {stats['average']:.2f}s")
            print(f"      📊 Min/Max: {stats['min']:.2f}s / {stats['max']:.2f}s")
            print(f"      🚀 Lưu lượng: {throughput:.2f} đơn/giây")
        
        print("\n" + "="*80 + "\n")


class PerformanceLogger:
    """Log hiệu suất vào file"""
    
    def __init__(self, filename="performance.log"):
        self.filename = filename
    
    def log_order(self, order_id, worker, duration, status):
        """Log một đơn hàng"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "order_id": order_id,
            "worker": worker,
            "duration": f"{duration:.2f}s",
            "status": status
        }
        
        with open(self.filename, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def read_logs(self):
        """Đọc tất cả log"""
        logs = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except FileNotFoundError:
            pass
        
        return logs
    
    def clear_logs(self):
        """Xóa log file"""
        try:
            open(self.filename, 'w').close()
            print(f"✅ Log file '{self.filename}' đã được xóa")
        except Exception as e:
            print(f"❌ Lỗi xóa log: {str(e)}")


if __name__ == "__main__":
    # Test performance tracker
    tracker = PerformanceTracker()
    
    # Simulate some data
    for i in range(1, 16):
        worker = f"Worker {(i % 3) + 1}"
        duration = (i * 0.5) % 5
        tracker.add_order_record(
            order_id=i,
            worker=worker,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            status="Completed",
            duration=duration
        )
    
    tracker.print_full_report()
