from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.db.order import Order
from app.exception.exceptions import OrderCreationException, OrderNotFoundException


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order_by_id(self, order_id: int):
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise OrderNotFoundException(f"Order not found with id {order_id}")
        return order

    def create_order(self, new_order: Order):
        try:
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
            return new_order

        except IntegrityError:
            self.db.rollback()
            raise OrderCreationException("Order Couldn't be created")
        except Exception as e:
            self.db.rollback()
            raise OrderCreationException("Order Couldn't be created")
