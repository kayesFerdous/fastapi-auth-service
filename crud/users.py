from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import defer, noload
from uuid import UUID

from schemas import UserCreate, UserUpdate
from models import User_db
from schemas.users import UserOut
from security.hashing import get_password_hash



async def get_user_by_email(email:str, db: AsyncSession) -> Optional[User_db]:
    result = await db.execute(
        select(User_db).filter(User_db.email == email)
    )
    return result.scalar_one_or_none()



async def get_users(db:AsyncSession) -> Optional[List[UserOut]]:
    result = await db.execute(
        select(User_db).options(noload(User_db.tasks), defer(User_db.password))
    )
    users = result.scalars().all()
    users = [UserOut.model_validate(user, from_attributes=True) for user in users]
    if not users:
        return None
    return users



async def get_user_by_id(user_id:UUID, db:AsyncSession) -> Optional[UserOut]:
    result = await db.execute(
        select(User_db).options(noload(User_db.tasks), defer(User_db.password)).filter(User_db.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return None
    return UserOut.model_validate(user, from_attributes=True)



async def delete_user(user_id:UUID, db:AsyncSession) -> Optional[UserOut]:
    result = await db.execute(
        select(User_db).filter(User_db.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
        return UserOut.model_validate(user, from_attributes=True)
    return None



async def create_user(user: UserCreate, db:AsyncSession) -> UserOut:
    new_user = User_db(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserOut.model_validate(new_user, from_attributes=True)



async def update_user(user_id: UUID, user: UserUpdate, db:AsyncSession) -> Optional[UserOut]:
    result = await db.execute(
        select(User_db).options(noload(User_db.tasks), defer(User_db.password)).filter(User_db.id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user:
        update_data = user.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == 'password':
                value = get_password_hash(value)
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return UserOut.model_validate(db_user, from_attributes=True)
    return None
