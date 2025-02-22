from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repository.metrics_repo import OrderMetricsRepository
from app.service.metrics_service import OrderMetricsService
from app.database import get_db

router = APIRouter(
    prefix="/metrics"
)


@router.get("")
def get_metrics(db: Session = Depends(get_db)):
    metrics_repo = OrderMetricsRepository(db)
    metrics_service = OrderMetricsService(metrics_repo)
    data = metrics_service.get_metrics()
    return data