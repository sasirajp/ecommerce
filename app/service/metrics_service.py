from app.repository.metrics_repo import OrderMetricsRepository
from app.models.dtos import MetricsReponse


class OrderMetricsService:

    def __init__(self, metrics_repo: OrderMetricsRepository):
        self.metrics_repo = metrics_repo

    def get_metrics(self):
        status_count = self.metrics_repo.get_count_orders_by_status()
        total_orders, avg_processing_time = self.metrics_repo.avg_processing_time()
        return MetricsReponse(
            status_count=status_count,
            avg_processing_time=avg_processing_time,
            total_orders=total_orders
        )
