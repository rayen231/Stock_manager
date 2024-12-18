from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx

# Initialize FastAPI app
app = FastAPI()

# Internal API URLs
PRODUCT_API_URL = "http://127.0.0.1:8083"
SUPPLIER_API_URL = "http://127.0.0.1:8082"

# Initialize httpx client for asynchronous requests
client = httpx.AsyncClient()

@app.get("/product/{path:path}")
async def proxy_product(path: str):
    try:
        response = await client.get(f"{PRODUCT_API_URL}/{path}")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error with product API: {exc}")

@app.get("/supplier/{path:path}")
async def proxy_supplier(path: str):
    try:
        response = await client.get(f"{SUPPLIER_API_URL}/{path}")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error with supplier API: {exc}")

# Start FastAPI server on 0.0.0.0 for external access
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
