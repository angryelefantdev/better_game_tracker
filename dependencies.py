from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from database import goonsession
from models.users import Users

import jwt


SECRET_KEY = "SECRETESTKEYS"
ALGORITHM = "HS256"

scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def getdb():
    db = goonsession()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: Annotated[str, Depends(scheme)],
    db = Depends(getdb)
):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401,detail="Invalid token")

        user = db.query(Users).filter(Users.name == username).first()

        if not user:
            raise HTTPException(status_code=401,detail="User doesn't exist")

        return user

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")