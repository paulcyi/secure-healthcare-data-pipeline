from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

# JWT settings
SECRET_KEY = "your-secret-key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize the FastAPI router
router = APIRouter()

# OAuth2 scheme for extracting the token from the request's Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pydantic models for the request body
class LoginModel(BaseModel):
    username: str
    password: str

class SignupModel(BaseModel):
    username: str
    password: str

# Utility functions for hashing and verifying passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Utility function to create JWT tokens
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to extract and verify JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# POST /signup route
@router.post("/signup")
async def signup(user: SignupModel):
    hashed_password = get_password_hash(user.password)
    # Save hashed password to your database (skipping actual DB logic for now)
    return {"message": "User signed up", "hashed_password": hashed_password}

# POST /login route
@router.post("/login")
async def login(user: LoginModel):
    # Example hashed password for demonstration (you'd retrieve this from your DB)
    stored_hashed_password = get_password_hash(user.password)

    # Compare entered password with stored hashed password
    if not verify_password(user.password, stored_hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create a JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


