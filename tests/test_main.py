import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_read_root():
    # Specify a full base_url with ASGITransport to avoid the URL issue
    async with AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Secure Healthcare Data Pipeline API"}



