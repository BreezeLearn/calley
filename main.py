from config.database import SessionLocal
from config.database import engine
from config.database import Base
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.models import User
from Routes.bot import router as bot_router
from Routes.embedding_route import router as embedding_router
from Routes.google_auth import router as google_auth_router
from typing import Annotated
from auth.auth_bearer import get_current_user
from pydantic import BaseModel
from config.db import get_db
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

class Login(BaseModel):
    email: str
    password: str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name=Login)

# JWT setup
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="add any string...")
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "https://example.com",
    "https://subdomain.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to get user by username
def get_user(db, email: str):
    return db.query(User).filter(User.email == email).first()


# Function to authenticate user
def authenticate_user(db, email: str, password: str):
    
    user = get_user(db, email)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    # Convert User object to dictionary
    if isinstance(to_encode['sub'], User):
        to_encode['sub'] = to_encode['sub'].username

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoints
@app.post("/signup/")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    if get_user(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create new user
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


    
@app.post("/login/")
def login(form_data: Login, db: Session = Depends(get_db)):
    print(form_data)
    user = authenticate_user(db, form_data.email, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/me/")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

app.include_router(bot_router)
app.include_router(embedding_router)
app.include_router(google_auth_router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)