from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.users import Users
from schemas.users import UserCreate, UserRequest,UserUpdate

from dependencies import getdb, get_current_user
from models.games import Games


router = APIRouter()


@router.get("/{user_id}", response_model=UserRequest)
def seeusers(
    user_id: int,
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):

    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User doesn't exist."
        )

    return user


@router.put("/{user_id}", response_model=UserRequest)
def updateuser(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):

    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User doesn't exist."
        )

    user.name = user_data.name

    db.commit()
    db.refresh(user)

    return user


@router.delete("/me")
def delete_my_account(
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):
    db.query(Games).filter(
        Games.user_id == current_user.id
    ).delete()

    db.delete(current_user)
    db.commit()

    return {"message": "Account and games deleted"}