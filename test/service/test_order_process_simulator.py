import pytest
import time
import threading
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.service.order_process_simulator import fetch_pending_orders, simulate_processing, retry_processing, order_queue
from app.models.db.order import Order
from app.models.dtos import OrderStatus


@pytest.fixture
def mock_session():
    mock_db = MagicMock()
    return mock_db


@pytest.fixture
def mock_order():
    return Order(order_id=1, status=OrderStatus.PENDING, updated_at=datetime.now())



@patch("app.database.SessionLocal")
def test_simulate_processing(mock_session_local, mock_session, mock_order):
    mock_session_local.return_value = mock_session
    mock_session.query.return_value.filter.return_value.first.return_value = mock_order

    order_queue.put(1)

    stop_event = threading.Event()
    worker_thread = threading.Thread(target=simulate_processing, args=(stop_event,), daemon=True)

    worker_thread.start()
    time.sleep(2)
    stop_event.set()
    worker_thread.join()

    assert mock_order.status == OrderStatus.PENDING

