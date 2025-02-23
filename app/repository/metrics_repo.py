from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.db.order import Order
from app.models.dtos import OrderByStatusCount, OrderStatus


class OrderMetricsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_count_orders_by_status(self):
        result = (
            self.db.query(Order.status, func.count(Order.status))
            .group_by(Order.status)
            .all()
        )
        return OrderByStatusCount(
            count={OrderStatus(status): count for status, count in result}
        )

    def avg_processing_time(self):
        orders_count = self.db.query(func.count(Order.order_id)).scalar()
        avg_processing_time = self.db.query(func.avg(extract("epoch", Order.updated_at - Order.created_at))) \
            .filter(Order.status == OrderStatus.COMPLETED) \
            .scalar()
        return orders_count, avg_processing_time / 60 if avg_processing_time is not None else 0
