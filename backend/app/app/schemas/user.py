from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
  email: Optional[str] = None
  is_active: Optional[bool] = True
  is_superuser: Optional[bool] = False
  full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
  email: str
  password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
  password: Optional[str] = None


class UserBaseInDB(UserBase):
  id: int = None

  class Config:
    orm_mode = True


# Additional properties to return via API
class User(UserBaseInDB):
  pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
  hashed_password: str
