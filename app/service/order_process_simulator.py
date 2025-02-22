import random
import threading
import time
from datetime import datetime, timedelta
import pytz

from app.models.db.order import Order
from app.models.dtos import OrderStatus
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import queue

order_queue = queue.Queue()


def fetch_pending_orders():
    print("loading orders to queue at", datetime.now(pytz.timezone('Asia/Kolkata')))
    db = SessionLocal()
    try:
        pending_order = db.query(Order).filter(Order.status == OrderStatus.PENDING).all()
        for order in pending_order:
            order_queue.put(order.order_id)
        print(f"{len(pending_order)} Order added in queue")
    except SQLAlchemyError as e:
        print("SQL exception ", e)
    finally:
        db.close()

    threading.Timer(20, fetch_pending_orders).start()


def simulate_processing():
    while True:
        try:
            if order_queue.empty():
                print("No Orders found to process")
                time.sleep(10)
                continue

            order_id = order_queue.get()
            db = SessionLocal()
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if order and order.status == OrderStatus.PENDING:
                order.status = OrderStatus.PROCESSING
                db.commit()
                time.sleep(random.randint(2, 7))
                order.status = OrderStatus.COMPLETED
                db.commit()
                db.close()
        except SQLAlchemyError as e:
            print("SQL Exception", e)


def retry_processing():
    db = SessionLocal()
    time_threshold = datetime.now() - timedelta(minutes=10)
    retry_orders = []
    try:
        pending_order = db.query(Order)\
            .filter(Order.status == OrderStatus.PROCESSING)\
            .filter(Order.updated_at < time_threshold)\
            .all()
        for order in pending_order:
            retry_orders.append(order.order_id)
            order.status = OrderStatus.PENDING
        db.commit()
        print(f" added these {retry_orders} orders for retry")
    except SQLAlchemyError as e:
        print("SQL exception ", e)
    finally:
        db.close()

    threading.Timer(600, retry_processing).start()


def start_order_processing():
    fetch_pending_orders()
    retry_processing()

    for _ in range(1):
        worker_thread = threading.Thread(target=simulate_processing, daemon=True)
        worker_thread.start()
