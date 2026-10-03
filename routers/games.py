from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models.games import Games
from schemas.game import GameCreate, GameRequest

from dependencies import getdb, get_current_user

from services.rawgio import search_game, get_game_details


router = APIRouter()


@router.get("/", response_model=List[GameRequest])
def seegames(
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):
    games = db.query(Games).filter(
        Games.user_id == current_user.id
    ).all()

    return games


@router.post("/", response_model=GameRequest)
def addgame(
    game: GameCreate,
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):

    results = search_game(game.name)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Game was not found on RAWG."
        )

    rawg_id = results[0]["id"]

    existing_game = db.query(Games).filter(
        Games.rawg_id == rawg_id
    ).first()

    if existing_game:
        raise HTTPException(
            status_code=400,
            detail="Game already exists in the database."
        )

    details = get_game_details(rawg_id)

    if not details:
        raise HTTPException(
            status_code=502,
            detail="Could not get game details from RAWG."
        )

    genres = details.get("genres", [])

    if genres:
        genre = genres[0]["name"]
    else:
        genre = "Unknown"

    developers = details.get("developers", [])

    if developers:
        developer = developers[0]["name"]
    else:
        developer = "Unknown"

    rating = details.get("rating")

    if rating is None:
        rating = 0.0


    newgame = Games(
        name=details["name"],
        genre=genre,
        rating=rating,
        developer=developer,
        rawg_id=rawg_id,
        user_id=current_user.id
    )

    db.add(newgame)
    db.commit()
    db.refresh(newgame)

    return newgame


@router.put("/{game_id}", response_model=GameRequest)
def updategame(
    game_id: int,
    gamer: GameCreate,
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):

    game = db.query(Games).filter(
        Games.id == game_id
    ).first()

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game doesn't exist."
        )

    for field, value in gamer.model_dump().items():
        setattr(game, field, value)

    db.commit()
    db.refresh(game)

    return game


@router.delete("/{game_id}")
def deletegame(
    game_id: int,
    db: Session = Depends(getdb),
    current_user=Depends(get_current_user)
):

    game = db.query(Games).filter(
        Games.id == game_id,
        Games.user_id == current_user.id
    ).first()

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game doesn't exist."
        )

    db.delete(game)
    db.commit()

    return {
        "message": "Deleted the game."
    }