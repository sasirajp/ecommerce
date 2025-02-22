from fastapi.testclient import TestClient

from unittest.mock import MagicMock
import pytest

from app.routes.order_metrics_controller import router
from app.service.metrics_service import OrderMetricsService
from app.models.dtos import MetricsReponse, OrderByStatusCount, OrderStatus

client = TestClient(router)


@pytest.fixture
def mock_metric_service(mocker):
    mock_service = MagicMock(spec=OrderMetricsService)
    mocker.patch("app.routes.order_metrics_controller.OrderMetricsService", return_value=mock_service)
    return mock_service


def test_metric_data(mock_metric_service):
    metrics_response = {
        "status_count": {
            "count": {
                "PENDING": 10,
                "COMPLETED": 2
            }
        },
        "total_orders": 10,
        "avg_processing_time": 2.0
    }
    mock_metric_service.get_metrics.return_value = MetricsReponse(
        status_count=OrderByStatusCount(count={
            OrderStatus.PENDING: 10,
            OrderStatus.COMPLETED: 2
        }),
        total_orders=10,
        avg_processing_time=2.0
    )
    response = client.get("/metrics")
    print(response)
    assert response.status_code == 200
    assert response.json() == metrics_response
