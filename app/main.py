from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from app.auth.auth import router as auth_router
from app.routers.data import router as data_router

# Loguru configuration
logger.add("logs.log", rotation="500 MB")

app = FastAPI(
    title="Secure Healthcare Data Pipeline API",
    description="An API for securely ingesting and retrieving healthcare data with HIPAA compliance monitoring.",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Root endpoint
@app.get("/")
async def read_root():
    logger.info("Root endpoint was called")
    return {
        "message": "Welcome to the Secure Healthcare Data Pipeline API",
        "documentation": "/docs",
        "endpoints": {
            "auth": {
                "login": "/auth/login",
                "signup": "/auth/signup"
            },
            "data": {
                "patients": "/data/patients",
                "patient_metrics": "/data/metrics/{patient_id}",
                "system_stats": "/data/stats"
            }
        }
    }

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(data_router, prefix="/data", tags=["Data"])

# Store the original openapi method
original_openapi = app.openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = original_openapi()
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi











