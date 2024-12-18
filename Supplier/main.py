from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from SupplierManager import SupplierManager
from fastapi import HTTPException
from pydantic import BaseModel


class Supplier(BaseModel):
    ID: int
    Name: str
    Adress: str  # We will convert this from datetime to string
    Contact: int

manager = SupplierManager()
app = FastAPI()  # Changed from App to app

origins = ["*"]  # Replace * with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/suppliers", response_model=List[Supplier])
def get_suppliers():
    return manager.read_supplier()

@app.get("/suppliers/{supplier_id}", response_model=Supplier)
def get_supplier(supplier_id: int):
    supplier = manager.read_supplier(supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@app.post("/suppliers")
def create_supplier(supplier: Supplier):
    return manager.create_supplier(supplier.Name, supplier.Adress, supplier.Contact)

@app.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, supplier: Supplier):
    return manager.update_supplier(supplier_id, supplier.Name, supplier.Adress, supplier.Contact)

@app.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int):
    return manager.delete_supplier(supplier_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8084)  # Changed from App to app