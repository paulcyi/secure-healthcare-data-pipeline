from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from app.auth.auth import get_current_user  # Import the authentication function to protect the route

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

# Protected GET /data/protected-endpoint route
@router.get("/protected-endpoint")
async def protected_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected endpoint", "user": current_user}

