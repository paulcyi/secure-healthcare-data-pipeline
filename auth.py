from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for the request body
class LoginModel(BaseModel):
    username: str
    password: str

class SignupModel(BaseModel):
    username: str
    password: str

# POST /signup route
@router.post("/signup")
async def signup(user: SignupModel):
    return {"message": "User signed up"}

# POST /login route
@router.post("/login")
async def login(user: LoginModel):
    return {"message": "User logged in"}
