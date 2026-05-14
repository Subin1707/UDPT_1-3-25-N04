import pika
import redis
import json
import random
import time
from datetime import datetime

# =========================
# RabbitMQ Connection
# =========================
rabbit_connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost"
    )
)

channel = rabbit_connection.channel()

channel.queue_declare(
    queue="order_queue",
    durable=True
)

# Worker chỉ nhận 1 task mỗi lần
channel.basic_qos(prefetch_count=1)

# =========================
# Redis Connection
# =========================
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# =========================
# Worker Name
# =========================
worker_name = input("Enter worker name: ")


# =========================
# Process Order Callback
# =========================
def process_order(ch, method, properties, body):

    order = json.loads(body)

    order_id = order["id"]

    start_time = datetime.now()

    print("\n==============================")
    print(
        f"[{worker_name}] "
        f"Processing order #{order_id}"
    )

    print(
        f"Customer: {order['customer']}"
    )

    print(
        f"Quantity: {order['quantity']}"
    )

    # Update trạng thái
    order["status"] = "Processing"

    # Giả lập xử lý
    process_time = random.randint(1, 5)

    print(
        f"Processing time: "
        f"{process_time}s"
    )

    time.sleep(process_time)

    # Completed
    order["status"] = "Completed"

    end_time = datetime.now()

    duration = (
        end_time - start_time
    ).seconds

    print(
        f"[{worker_name}] "
        f"Completed order #{order_id}"
    )

    print(
        f"Total time: {duration}s"
    )

    # =========================
    # Publish notification
    # =========================
    redis_client.publish(
        "order_channel",
        json.dumps({
            "order_id": order_id,
            "status": "Completed",
            "worker": worker_name
        })
    )

    # ACK message
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


# =========================
# Consume Queue
# =========================
channel.basic_consume(
    queue="order_queue",
    on_message_callback=process_order
)

print(
    f"\n[{worker_name}] "
    f"Waiting for orders..."
)

channel.start_consuming()