from app.repository.order_repo import OrderRepository
from app.models.dtos import OrderCreate
from app.models.db.order import Order
from app.models.dtos import OrderStatus


class OrderService:

    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get_order_by_id(self, order_id: int):
        return self.order_repository.get_order_by_id(order_id)

    def create_order(self, order: OrderCreate):
        new_order = Order(
            user_id=order.user_id,
            item_ids=order.item_ids,
            total_amount=order.total_amount,
            status=OrderStatus.PENDING
        )
        return self.order_repository.create_order(new_order)
