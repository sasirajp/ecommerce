import pytest
from unittest.mock import MagicMock
from app.service.order_service import OrderService
from app.repository.order_repo import OrderRepository
from app.models.db.order import Order, OrderStatus
from app.models.dtos import OrderCreate


@pytest.fixture
def mock_order_repository():
    mock_repo = MagicMock(spec=OrderRepository)
    return mock_repo


@pytest.fixture
def order_service(mock_order_repository):
    return OrderService(mock_order_repository)


def test_get_order_by_id(order_service, mock_order_repository):
    mock_order = Order(order_id=1, user_id=101, item_ids=[1, 2, 3], total_amount=250, status=OrderStatus.PENDING)
    mock_order_repository.get_order_by_id.return_value = mock_order
    result = order_service.get_order_by_id(1)
    assert result == mock_order


def test_create_order(order_service, mock_order_repository):
    order_data = OrderCreate(user_id=102, item_ids=[4, 5], total_amount=150)
    mock_order = Order(order_id=2, user_id=102, item_ids=[4, 5], total_amount=150, status=OrderStatus.PENDING)
    mock_order_repository.create_order.return_value = mock_order
    result = order_service.create_order(order_data)
    assert result == mock_order
    assert result.user_id == 102
    assert result.status == OrderStatus.PENDING
