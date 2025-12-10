"""
Demo FastAPI server with in-memory storage for preview/testing
This server doesn't require MongoDB and stores data in memory
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
import uuid

# JWT Configuration
JWT_SECRET = 'dev-secret-key-for-demo-12345'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer()

# Create the main app
app = FastAPI(title="ERP Inventory Management System - Demo")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_db = {}
items_db = {}
categories_db = {}
suppliers_db = {}
warehouses_db = {}
purchase_orders_db = {}

# ============ Models ============
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "Admin"
    department: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str
    department: Optional[str] = None
    is_active: bool = True
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class ItemCategory(BaseModel):
    id: str
    code: str
    name: str
    parent_category: Optional[str] = None
    is_active: bool = True

class ItemMaster(BaseModel):
    id: str
    item_code: str
    item_name: str
    category_id: str
    uom: str
    is_active: bool = True

# ============ Authentication ============
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user_id: str) -> str:
    """Create JWT access token."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Verify JWT token and return current user."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id or user_id not in users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return users_db[user_id]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============ Routes ============
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ERP Inventory Management System - Demo API",
        "status": "running",
        "mode": "in-memory (no database required)"
    }

@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    for uid, user in users_db.items():
        if isinstance(user, User) and user.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_data.password)

    user = User(
        id=user_id,
        email=user_data.email,
        name=user_data.name,
        role=user_data.role,
        department=user_data.department,
        created_at=datetime.now(timezone.utc)
    )

    # Store user with password
    users_db[user_id] = user
    users_db[f"{user_id}_pwd"] = hashed_pwd

    # Create access token
    access_token = create_access_token(user_id)

    return Token(access_token=access_token, token_type="bearer", user=user)

@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user."""
    # Find user by email
    user = None
    user_id = None
    for uid, u in users_db.items():
        if isinstance(u, User) and u.email == credentials.email:
            user = u
            user_id = uid
            break

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    stored_pwd = users_db.get(f"{user_id}_pwd")
    if not stored_pwd or not verify_password(credentials.password, stored_pwd):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(user_id)

    return Token(access_token=access_token, token_type="bearer", user=user)

@app.get("/api/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

# ============ Masters API ============
@app.get("/api/masters/item-categories")
async def get_categories(current_user: User = Depends(get_current_user)):
    """Get all item categories."""
    return list(categories_db.values())

@app.post("/api/masters/item-categories")
async def create_category(category: ItemCategory, current_user: User = Depends(get_current_user)):
    """Create a new category."""
    categories_db[category.id] = category
    return category

@app.get("/api/masters/items")
async def get_items(current_user: User = Depends(get_current_user)):
    """Get all items."""
    return list(items_db.values())

@app.post("/api/masters/items")
async def create_item(item: ItemMaster, current_user: User = Depends(get_current_user)):
    """Create a new item."""
    items_db[item.id] = item
    return item

@app.get("/api/masters/suppliers")
async def get_suppliers(current_user: User = Depends(get_current_user)):
    """Get all suppliers."""
    return []

@app.get("/api/masters/warehouses")
async def get_warehouses(current_user: User = Depends(get_current_user)):
    """Get all warehouses."""
    return []

@app.get("/api/masters/uoms")
async def get_uoms(current_user: User = Depends(get_current_user)):
    """Get all UOMs."""
    return []

# Create demo admin user on startup
@app.on_event("startup")
async def create_demo_user():
    """Create a demo admin user."""
    demo_user_id = str(uuid.uuid4())
    demo_user = User(
        id=demo_user_id,
        email="admin@demo.com",
        name="Demo Admin",
        role="Admin",
        created_at=datetime.now(timezone.utc)
    )
    users_db[demo_user_id] = demo_user
    users_db[f"{demo_user_id}_pwd"] = hash_password("admin123")

    print("=" * 60)
    print("Demo user created:")
    print("  Email: admin@demo.com")
    print("  Password: admin123")
    print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
