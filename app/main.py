from fastapi import FastAPI
from app.auth.auth import router as auth_router  # Import your authentication router
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
    
    # Set the global security scheme to require BearerAuth for all routes
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema  # Store the schema
    return app.openapi_schema

# Override the default openapi method with the custom one
app.openapi = custom_openapi









