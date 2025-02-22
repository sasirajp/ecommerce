from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.exception.exceptions import OrderCreationException, OrderNotFoundException


def register_exception_handler(app: FastAPI):

    @app.exception_handler(OrderCreationException)
    def order_creation_exception(req: Request, exception: OrderCreationException):
        return JSONResponse(status_code=400, content=exception.message)

    @app.exception_handler(OrderNotFoundException)
    def order_creation_exception(req: Request, exception: OrderNotFoundException):
        return JSONResponse(status_code=404, content=exception.message)

    @app.exception_handler(Exception)
    def order_creation_exception(req: Request, exception: Exception):
        return JSONResponse(status_code=500, content=f"Internal server error {exception}")
