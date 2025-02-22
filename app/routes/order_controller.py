from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.dtos import OrderResponse, OrderCreate
from app.service.order_service import OrderService
from app.repository.order_repo import OrderRepository

router = APIRouter(
    prefix="/order"
)


@router.post("/create_order", response_model=OrderResponse)
def order_controller(order: OrderCreate, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    return order_service.create_order(order)


@router.get("/get_order/{order_id}", response_model=OrderResponse)
def order_controller(order_id: int, db: Session = Depends(get_db)):
    order_repository = OrderRepository(db)
    order_service = OrderService(order_repository)
    return order_service.get_order_by_id(order_id)


