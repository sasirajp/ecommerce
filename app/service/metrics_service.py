from app.repository.metrics_repo import OrderMetricsRepository


class OrderMetricsService:
    
    def __init__(self, metrics_repo: OrderMetricsRepository):
        self.metrics_repo = metrics_repo
    
    def get_metrics(self):
        return self.metrics_repo.get_count_orders_by_status()
    