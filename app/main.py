from fastapi import FastAPI
from app.auth import auth as auth_router  # Import your authentication router
from app.routers.data import router as data_router  # Import your data router

app = FastAPI(
    title="Secure Healthcare Data Pipeline API",
    description="An API for securely ingesting and retrieving healthcare data.",
    version="0.1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Secure Healthcare Data Pipeline API"}

# Include the authentication router
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

# Include the data router
app.include_router(data_router, prefix="/data", tags=["Data"])

