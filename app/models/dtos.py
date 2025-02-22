import enum
from pydantic import BaseModel


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


class OrderCreate(BaseModel):
    user_id: int
    item_ids: list[int]
    total_amount: float


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    item_ids: list[int]
    total_amount: float
    status: OrderStatus

    class Config:
        from_attributes = True


class OrderByStatusCount(BaseModel):
    count: dict[OrderStatus, int]