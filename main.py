import json
import re
import uuid
from pathlib import Path as FilePath
from datetime import date
from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException, status, Path, Query
from pydantic import BaseModel, EmailStr, Field, field_validator, computed_field
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='User Management App',
    description='API managing user data with validation',
    version='1.0.0'
)

# Serve static files for UI
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON File DB Path
DB_PATH = FilePath("users_db.json")

# ----------------------------
# Base User model
# ----------------------------
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100, pattern=r"^[a-zA-Z\s]+$")
    email: EmailStr
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    username: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    date_of_birth: Optional[date] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    accept_marketing_emails: bool = False

    @field_validator('phone_number')
    def validate_phone(cls, value):
        if value is None:
            return value
        if not re.match(r"^\+?\d{10,15}$", value):
            raise ValueError('Phone number is invalid')
        return value

    @field_validator('email')
    def validate_emails(cls, value):
        valid_domains = ['gmail.com', 'hotmail.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Email must be from gmail.com or hotmail.com')
        return value

    @computed_field
    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            today = date.today()
            years = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                years -= 1
            return years
        return None

# ----------------------------
# Model for User Creation
# ----------------------------
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[0-9]", value):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        return value

# ----------------------------
# Model for Response
# ----------------------------
class UserResponse(UserBase):
    user_id: str

    class Config:
        from_attributes = True

# ----------------------------
# Load & Save DB
# ----------------------------
def load_db() -> dict:
    if not DB_PATH.exists():
        save_db({})
        return {}
    try:
        if DB_PATH.stat().st_size == 0:
            return {}
        with open(DB_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            return {k: UserResponse(**v) for k, v in raw.items()}
    except json.JSONDecodeError:
        save_db({})
        return {}

def save_db(users: dict):
    temp_path = DB_PATH.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump({k: v.model_dump(mode="json") for k, v in users.items()}, f, indent=2)
    temp_path.replace(DB_PATH)

users_db = load_db()

# ----------------------------
# Serve UI
# ----------------------------
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# ----------------------------
# CRUD Endpoints
# ----------------------------
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    if user.email in [u.email for u in users_db.values()]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_data = user.model_dump()
    user_data["user_id"] = user_id
    new_user = UserResponse(**user_data)
    users_db[user_id] = new_user
    save_db(users_db)
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str = Path(..., pattern=r"^[0-9a-f-]{36}$")):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.get("/user/", response_model=List[UserResponse])
async def list_user(country: Optional[str] = Query(None), min_age: Optional[int] = Query(None), max_age: Optional[int] = Query(None)):
    filtered_users = list(users_db.values())
    if country:
        filtered_users = [u for u in filtered_users if u.country == country]
    if min_age is not None:
        filtered_users = [u for u in filtered_users if u.age and u.age >= min_age]
    if max_age is not None:
        filtered_users = [u for u in filtered_users if u.age and u.age <= max_age]
    return filtered_users

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del users_db[user_id]
    save_db(users_db)
    return {"msg": "User deleted"}
