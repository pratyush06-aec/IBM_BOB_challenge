"""
Authentication Service
Handles user authentication, registration, and JWT token management
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """User model"""
    id: str
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    disabled: bool = False


class UserInDB(User):
    """User model with hashed password"""
    hashed_password: str


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


class UserCreate(BaseModel):
    """User registration model"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str


# In-memory user storage (replace with database in production)
fake_users_db = {}


class AuthService:
    """Service for handling authentication"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password (bcrypt has 72 byte limit)"""
        # Truncate password to 72 bytes if necessary
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)
    
    @staticmethod
    def get_user(username: str) -> Optional[UserInDB]:
        """Get user from database"""
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)
        return None
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user"""
        user = AuthService.get_user(username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenData]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None or not isinstance(username, str):
                return None
            return TokenData(username=username)
        except JWTError:
            return None
    
    @staticmethod
    def register_user(user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        if user_data.username in fake_users_db:
            raise ValueError("Username already registered")
        
        if any(u['email'] == user_data.email for u in fake_users_db.values()):
            raise ValueError("Email already registered")
        
        # Create user
        user_id = f"user_{len(fake_users_db) + 1}"
        hashed_password = AuthService.get_password_hash(user_data.password)
        
        user_dict = {
            'id': user_id,
            'email': user_data.email,
            'username': user_data.username,
            'full_name': user_data.full_name,
            'hashed_password': hashed_password,
            'disabled': False
        }
        
        fake_users_db[user_data.username] = user_dict
        
        return User(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            disabled=False
        )
    
    @staticmethod
    def get_current_user(token: str) -> Optional[User]:
        """Get current user from token"""
        token_data = AuthService.decode_token(token)
        if token_data is None or token_data.username is None:
            return None
        
        user = AuthService.get_user(token_data.username)
        if user is None:
            return None
        
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            disabled=user.disabled
        )


# Demo user will be created on first startup via API
# Use POST /api/auth/register with:
# {
#   "username": "demo",
#   "email": "demo@graphmind.ai",
#   "password": "demo123",
#   "full_name": "Demo User"
# }

# Made with Bob