from pydantic import BaseModel,Field

class GameRequest(BaseModel):
    id:int
    name:str
    genre:str
    rating:float
    developer:str
    rawg_id:int
    user_id:int

    class Config:
        from_attributes = True

class GameCreate(BaseModel):
    name:str = Field(...,min_length=3,max_length=100,description="The Name of the Game.")