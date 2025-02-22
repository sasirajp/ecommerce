from unittest.mock import MagicMock
import pytest

from app.repository.metrics_repo import OrderMetricsRepository
from app.service.metrics_service import OrderMetricsService
from app.models.dtos import OrderByStatusCount, MetricsReponse, OrderStatus


@pytest.fixture()
def mock_metric_repo_fixture(mocker):
    mock_repo = MagicMock(spec=OrderMetricsRepository)
    mock_repo.get_count_orders_by_status.return_value = OrderByStatusCount(count = {
        OrderStatus.PENDING: 2,
        OrderStatus.COMPLETED: 2
    })
    mock_repo.avg_processing_time.return_value = (10, 22.1)
    return mock_repo


@pytest.fixture()
def order_metric_service(mock_metric_repo_fixture):
    return OrderMetricsService(mock_metric_repo_fixture)


def test_get_metrics(order_metric_service):
    metrics_response = MetricsReponse(
        status_count=OrderByStatusCount(count={
            OrderStatus.PENDING: 2,
            OrderStatus.COMPLETED: 2
        }),
        total_orders=10,
        avg_processing_time=22.1
    )
    result = order_metric_service.get_metrics()

    assert result == metrics_response
