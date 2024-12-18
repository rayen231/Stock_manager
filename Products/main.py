from ProductsManager import ProductsManager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import uvicorn


app = FastAPI()
manager = ProductsManager()
origins = ["*"]
CORSMiddleware(app, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Product(BaseModel):
    ID: int
    Name: str
    Type: str  # We will convert this from datetime to string
    Price: float
    SupplierID: int
    Quantity: int

@app.get("/products", response_model=List[Product])
def get_products():
    return manager.read_products()


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = manager.read_products(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/create", response_model=str)
def create_product(product: Product):
        return manager.create_product(product.Name, product.Type, product.Price, product.Quantity, product.SupplierID)

@app.put("/products/update/{product_id}", response_model=str)
def update_product(product_id: int, product: Product):
    updated_product = manager.update_product(product_id, name=product.Name, type=product.Type, price=product.Price, quantity=product.Quantity, supplier_id=product.SupplierID)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/delete/{product_id}", response_model=str)
def delete_product(product_id: int):
    deleted_product = manager.delete_product(product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product

@app.get("/alerts", response_model=List[Product])
def get_alerts():
    return manager.alert()

if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8083)