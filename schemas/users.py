from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from enum import StrEnum

from schemas.task import Task


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


# Base schema with common attributes, password is not included
class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.USER


# Schema for creating a user, inherits from UserBase and adds the password
class UserCreate(UserBase):
    password: str


# Schema for updating a user, all fields are optional
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


# Schema for reading/returning a user from the API, omits password
class User(UserBase):
    id: UUID
    tasks: List[Task] = []

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
