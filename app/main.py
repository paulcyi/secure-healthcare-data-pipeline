from fastapi import FastAPI
from loguru import logger  # Import Loguru
from prometheus_fastapi_instrumentator import Instrumentator
from app.auth.auth import router as auth_router  # Import your authentication router
from app.routers.data import router as data_router  # Import your data router

# Loguru configuration (optional: you can customize this further)
logger.add("logs.log", rotation="500 MB")  # Logs will be saved to a file with log rotation

app = FastAPI(
    title="Secure Healthcare Data Pipeline API",
    description="An API for securely ingesting and retrieving healthcare data.",
    version="0.1.0"
)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def read_root():
    logger.info("Root endpoint was called")
    return {"message": "Welcome to the Secure Healthcare Data Pipeline API"}

# Example of a data ingestion endpoint
@app.post("/data/ingest")
async def ingest_data():
    logger.info("Data ingestion endpoint was called")
    return {"message": "Healthcare data has been ingested successfully"}

# Example of an error handling endpoint
@app.get("/data/error")
async def simulate_error():
    try:
        # Simulating an error for logging purposes
        1 / 0  # Division by zero error
    except ZeroDivisionError as e:
        logger.error(f"An error occurred during data processing: {e}")
        return {"error": "An internal error occurred while processing data"}

# Include the authentication router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include the data router
app.include_router(data_router, prefix="/data", tags=["Data"])

# Store the original openapi method in a separate variable before overriding
original_openapi = app.openapi

# Custom OpenAPI function to declare Bearer Authentication in Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema  # Return the schema if it already exists
    
    # Call the original FastAPI openapi() function to generate the schema
    openapi_schema = original_openapi()
    
    # Define the security schema for Bearer Auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add security requirements for Bearer Auth
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema  # Store the generated schema in the app object
    return app.openapi_schema

# Override the default OpenAPI method with the custom one
app.openapi = custom_openapi












