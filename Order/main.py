from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel , Field
from OrderManager import OrderManager as ordermanager
import uvicorn

app = FastAPI()
ordermanager = ordermanager()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    ID: int
    Date: str  # We will convert this from datetime to string
    Total: int
    SupplierID: float
    Status: str


@app.get("/orders", response_model=List[Order])
def get_orders():
    return ordermanager.read_order()

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = ordermanager.read_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders", response_model=str)
def create_order(order: Order):
    return ordermanager.create_order(order.Date, order.Total, order.SupplierID, order.Status)

@app.put("/orders/{order_id}", response_model=str)
def update_order(order_id: int, order: Order):
    updated_order = ordermanager.update_order(order_id, date=order.Date, total=order.Total, supplier_id=order.SupplierID, status=order.Status)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}", response_model=str)
def delete_order(order_id: int):
    deleted_order = ordermanager.delete_order(order_id)
    if deleted_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8082)