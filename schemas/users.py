from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The Name of the User."
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="The Password of the User."
    )


class UserUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The new username."
    )