from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

# Initialize the FastAPI router
router = APIRouter()

# Simulated in-memory database and ID counter
database: Dict[int, dict] = {}
id_counter = 1

# Pydantic models for request validation and data structure
class DataIngestionModel(BaseModel):
    patient_id: int
    data: str

class DataRetrievalModel(BaseModel):
    id: int
    patient_id: int
    data: str

# POST /data route for ingesting new healthcare data
@router.post("/data")
async def ingest_data(data: DataIngestionModel):
    global id_counter
    # Create a new entry with a unique ID
    new_entry = {
        "id": id_counter,
        "patient_id": data.patient_id,
        "data": data.data
    }
    # Store the new entry in the simulated database
    database[id_counter] = new_entry
    id_counter += 1
    return new_entry

# GET /data/{id} route for retrieving healthcare data by ID
@router.get("/data/{id}")
async def retrieve_data(id: int):
    if id not in database:
        raise HTTPException(status_code=404, detail="Data not found")
    return database[id]

# Initialize the FastAPI app
app = FastAPI()

# Include the router in the app
app.include_router(router)

# Add a simple root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Secure Healthcare Data API"}