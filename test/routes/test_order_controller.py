from fastapi.testclient import TestClient

from unittest.mock import MagicMock
import pytest

from app.routes.order_controller import router
from app.service.order_service import OrderService
from app.models.dtos import OrderResponse, OrderStatus

client = TestClient(router)


@pytest.fixture
def mock_order_service(mocker):
    mock_service = MagicMock(spec=OrderService)
    mocker.patch("app.routes.order_controller.OrderService", return_value=mock_service)
    return mock_service


def test_create_order(mock_order_service):
    order_data = {
        "user_id": 101,
        "item_ids": [1, 2, 3],
        "total_amount": 250.0
    }
    mock_order_service.create_order.return_value = OrderResponse(
        order_id=1, user_id=101, item_ids=[1, 2, 3], total_amount=250.0, status=OrderStatus.PENDING
    )
    response = client.post("/order/create_order", json=order_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == 101


def test_get_order(mock_order_service):
    mock_order_service.get_order_by_id.return_value = OrderResponse(
        order_id=1, user_id=101, item_ids=[1, 2, 3], total_amount=250.0, status=OrderStatus.PENDING
    )
    response = client.get("/order/get_order/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 101


