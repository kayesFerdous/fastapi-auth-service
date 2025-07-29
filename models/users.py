from typing import List, TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import String, UUID as UUID_db
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from schemas.users import UserRole

if TYPE_CHECKING:
    from models.task import Task_db

class User_db(Base):
    __tablename__ = 'users'

    id:Mapped[UUID_db] = mapped_column(UUID_db(as_uuid=True), primary_key=True, default=uuid4)
    username:Mapped[str] = mapped_column(String, nullable=False)
    email:Mapped[str]= mapped_column(String,nullable=False)
    password:Mapped[str] = mapped_column(String, nullable=False)
    role:Mapped[UserRole] = mapped_column(String, nullable=False, default=UserRole.USER)

    tasks:Mapped[List["Task_db"]] = relationship("Task_db", back_populates='user')

