from fastapi import FastAPI

app = FastAPI(
    title="Secure Healthcare Data Pipeline API",
    description="An API for securely ingesting and retrieving healthcare data.",
    version="0.1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Secure Healthcare Data Pipeline API"}

# Include Routers (to be implemented in Step 2)

