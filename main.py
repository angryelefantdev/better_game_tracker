from fastapi import FastAPI,HTTPException,Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import jwt

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pydantic import BaseModel

password_haser = PasswordHash((Argon2Hasher(),))

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "#$##$#$#$"

ALGORITHM = "HS256"

db = {}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload["sub"]

        if username not in db:
            raise HTTPException(
                status_code=401,
                detail="User doesn't exist"
            )

        return username

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )



class User(BaseModel):
    username:str
    password:str

@app.post("/register")
def register(user:User):
    if user.username in db:
        raise HTTPException(status_code=400,detail="Already exists")
    hashed_pw = password_haser.hash(user.password)
    db[user.username] = {
        "username" : user.username,
        "password" : hashed_pw
    }
    return {"message":"yay"}

@app.post("/token")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = db.get(form_data.username)
    if not user or not password_haser.verify(form_data.password,user["password"]):
        raise HTTPException(status_code=401,detail="Forbidden")
    token = jwt.encode({"sub":user["username"]},SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":token,"token_type":"bearer"}

@app.get("/me")
def get_user(user = Depends(get_current_user)):
    return user
   
@app.get("/secret")
def secret(user = Depends(get_current_user)):
    
    return {"message": "you found the secret"}  
    