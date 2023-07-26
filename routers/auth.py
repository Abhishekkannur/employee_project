from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel, Field
from database import SessionLocal
from datetime import datetime,timedelta
import models
from cryptography.fernet import Fernet
from models import Register
from passlib.context import CryptContext
from typing import *
from sqlalchemy.orm import Session
from models import *
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
fernet_key = Fernet.generate_key()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = fernet_key
ALGORITHAM='HS256'
def authenticate_user(username:str,password:str,db):
    user=db.query(Register).filter(Register.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password):
        return False
    return user
def create_access_token(username : str, user_id:int, expires_delta: timedelta):
    user = db.query(Register).filter(Register.username == username).filter(Register.id == user_id).first()
    if not user:
        return None
    encode={'sub':username,'id':user_id}
    expires=datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHAM)
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHAM])
        username: str = payload.get('sub')
        user_id :int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
        return {'username':username, 'id':user_id}
    except JWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
async def get_current_employee(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHAM])
        username: str = payload.get('sub')
        user_id :int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
        return {'id':user_id}
    except JWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')

class user_request(BaseModel):
    username: str
    @validator('username')
    def validate_username(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError("last name must contain only alphabetic characters and spaces.")
        return value.strip()
    password: str



class user_login_request(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token:str
    token_type: str

@router.post("/create_user")
async def create_user(create_user_request: user_request, db: Session = Depends(get_db)):
    create_user_model = Register(
        username=create_user_request.username,
        password=bcrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(from_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db: Session = Depends(get_db)):
    user=authenticate_user(from_data.username,from_data.password,db)

    if not user:
        return  HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
    token=create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'access_token':token,'token_type':'Bearer'}
@router.get("/get_user", status_code=status.HTTP_200_OK)
async def read_all_user(db: Session = Depends(get_db)):
        return db.query(Register).all()
    
    
