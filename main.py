from fastapi import FastAPI
import uvicorn

from app.routes import order_controller, order_metrics_controller
from app.service.order_process_simulator import start_order_processing
from app.exception.exception_handler import register_exception_handler

app = FastAPI()

app.include_router(order_controller.router)
app.include_router(order_metrics_controller.router)
register_exception_handler(app)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


@app.on_event("startup")
def app_startup():
    start_order_processing()


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
