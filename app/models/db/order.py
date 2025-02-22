from .base import EcommerceBase, Base
from sqlalchemy import Column, Integer, ARRAY, Float, Enum
from app.models.dtos import OrderStatus


class Order(EcommerceBase):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    item_ids = Column(ARRAY(Integer), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
