import sys
import os
import pytest
from httpx import AsyncClient
from app.main import app

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Secure Healthcare Data Pipeline API"}

@pytest.mark.asyncio
async def test_ingest_data():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/data/ingest")
    assert response.status_code == 200
    assert response.json() == {"message": "Healthcare data has been ingested successfully"}

@pytest.mark.asyncio
async def test_simulate_error():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/data/error")
    assert response.status_code == 200
    assert response.json() == {"error": "An internal error occurred while processing data"}


