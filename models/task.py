from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import String, Boolean, UUID as UUID_db, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database import Base
from models.users import User_db

if TYPE_CHECKING:
    from models.task import User_db

class Task_db(Base):
    __tablename__ = 'tasks'

    id:Mapped[UUID_db] = mapped_column(UUID_db(as_uuid=True), primary_key=True, default=uuid4)
    title:Mapped[str] = mapped_column(String, nullable=False)
    description:Mapped[str] = mapped_column(String)
    is_done:Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    owner:Mapped[UUID_db] = mapped_column(UUID_db(as_uuid=True), ForeignKey('users.id'), nullable=False)

    user:Mapped["User_db"] = relationship('User_db', back_populates='tasks')
    



