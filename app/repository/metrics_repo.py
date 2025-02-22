from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.db.order import Order, OrderStatus
from app.models.dtos import OrderByStatusCount

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
            count  = {OrderStatus(status): count for status, count in result}
        )