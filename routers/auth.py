from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,HTTPException,Depends
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from database import Session
from dependencies import getdb,get_current_user
from schemas.users import UserCreate,UserRequest
from models.users import Users

SECRET_KEY = "SECRETESTKEYS"
ALGORITHM = "HS256"


password_hasher = PasswordHash((Argon2Hasher(),))

router = APIRouter()

@router.post("/register")
def register(user:UserCreate,db:Session = Depends(getdb)):
    usera = db.query(Users).filter(Users.name == user.name).first()
    if usera:
        raise HTTPException(status_code=400,detail="Already exists")
    hashed_pw = password_hasher.hash(user.password)
    new_user = Users(name=user.name,password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message":f"Created account for {new_user.name}"}

@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(getdb)):

    user = db.query(Users).filter(Users.name == form_data.username).first()

    if not user or not password_hasher.verify(form_data.password,user.password):
        raise HTTPException(status_code=401,detail="Incorrect username or password")

    token = jwt.encode({"sub": user.name},SECRET_KEY,algorithm=ALGORITHM)

    return {"access_token": token,"token_type": "bearer"}

@router.get("/me")
def getme(myself = Depends(get_current_user)):
    return myself.name,myself.id

