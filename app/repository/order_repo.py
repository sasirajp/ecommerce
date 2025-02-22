from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.db.order import Order
from fastapi import HTTPException, status


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order_by_id(self, order_id: int):
        return self.db.query(Order).filter(Order.order_id == order_id).first()
    
    def create_order(self, new_order: Order):
        try:
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database integrity error"
            )

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong: {str(e)}"
            )
        