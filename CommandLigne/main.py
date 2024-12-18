from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from CommandLigneManager import CommandLigneManager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
manager = CommandLigneManager()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandLigne(BaseModel):
    product_id: int
    date: str
    order_id: int
    box_quantity: int

@app.post("/commandligne/")
def create_commandligne(commandligne: CommandLigne):
    try:
        manager.create_commandligne(commandligne.product_id, commandligne.date, commandligne.order_id, commandligne.box_quantity)
        return {"message": "Command ligne created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/commandligne/{commandligne_id}")
def read_commandligne(commandligne_id: int):
    commandligne = manager.read_commandligne(commandligne_id)
    if commandligne:
        return commandligne
    else:
        raise HTTPException(status_code=404, detail="Command ligne not found")

@app.put("/commandligne/{commandligne_id}")
def update_commandligne(commandligne_id: int, commandligne: CommandLigne):
    try:
        manager.update_commandligne(commandligne_id, commandligne.product_id, commandligne.date, commandligne.order_id, commandligne.box_quantity)
        return {"message": "Command ligne updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/commandligne/{commandligne_id}")
def delete_commandligne(commandligne_id: int):
    try:
        manager.delete_commandligne(commandligne_id)
        return {"message": "Command ligne deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    manager.close_connection()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)