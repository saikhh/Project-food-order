import jwt 
from fastapi import Depends, HTTPException, status, APIRouter 
from fastapi.security import OAuth2PasswordBearer 
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError 
from passlib.context import CryptContext    
from datetime import datetime, timedelta,timezone 
from sqlalchemy.orm import Session 

from ..database import get_db 
from ..schemas import TokenData 
from ..models import User 

SECRET_KEY = "e5ed2fec6c87c8a74546400f61b374253c385f916396fb7cd36ffb24d5afcb51" # Secret key 

ALGORITHM = "HS256"  # Algorithm used for signing the JWT 
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Password hashing context 
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/token")  

router = APIRouter()  # Create a router for authentication endpoints


def verify_password(plain_password,hashed_password): 
    return pwd_context.verify(plain_password,hashed_password)  # Verify the provided password against the hashed password 

def get_password_hash(password): 
    return pwd_context.hash(password) # Hash the provided password 

def get_user(db: Session, username: str): 
    db_user=db.query(User).filter(User.username==username).first()
    return db_user  # Retrieve a user from the database by username

def authenticate_user(db:Session, username: str , password: str): 
    user=get_user(db,username) 
    if not user: 
        return False  # Return False if the user does not exist 
    if not verify_password(password,user.hashed_password): 
        return False  # Return False if the password is incorrect
    return user  # Return the user object if authentication is successful 

def create_access_token(data:dict, expires_delta:timedelta | None= None): 
    to_encode=data.copy()
    if expires_delta: 
        expire=datetime.now(timezone.utc)+expires_delta  # Set the expiration time for the token
    else: 
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)  # Default expiration time is 15 minutes    
    to_encode.update({"exp":expire})  # Add the expiration time to the token payload
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)    
    return encoded_jwt  # Return the encoded JWT token 

async def get_current_user(token:str =Depends(oauth2_scheme),db:Session=Depends(get_db)): 
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])  # Decode the JWT token
        username:str=payload.get("sub")  # Extract the username from the token payload
        if username is None: 
            raise credentials_exception  # Raise an exception if the username is not found
        token_data=TokenData(username=username)  # Create a TokenData object with the username
    except InvalidTokenError: 
        raise credentials_exception  # Raise an exception if the token is invalid

    user=db.query(User).filter(User.username == token_data.username).first()  # Retrieve the user from the database
    if user is None: 
        raise credentials_exception  # Raise an exception if the user is not found      
    return user  # Return the authenticated user object 

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user  # Return the current active user object