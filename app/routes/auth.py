# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.models import UserModel
from app.database import db
from app.utils import get_password_hash, verify_password, create_access_token, verify_token
from pymongo.errors import DuplicateKeyError

router = APIRouter()

users_collection = db.users
users_collection.create_index("username", unique=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    if user.password != user.repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(user.password)
    new_user = UserModel(email=user.email, username=user.username, hashed_password=hashed_password)
    
    try:
        users_collection.insert_one(new_user.dict())
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return UserResponse(username=new_user.username, email=new_user.email)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = users_collection.find_one({"username": form_data.username})
    
    if db_user is None or not verify_password(form_data.password, db_user['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": db_user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
