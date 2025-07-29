from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from schemas import UserCreate, UserUpdate, UserOut
from crud.users import create_user, get_user_by_id, get_users, delete_user, update_user, get_user_by_email
from database import get_db
from schemas.users import User
from security.roles import admin_required
from security.token import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def read_all_users(db: AsyncSession = Depends(get_db), _:User=Depends(admin_required)):
    return await get_users(db)



@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:

    print(f'IN the route: {new_user.email}')
    db_user = await get_user_by_email(new_user.email, db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    return await create_user(new_user, db)



@router.get('/{user_id}', response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user



"""
********************* TODO *********************

GET /users/{user_id} and DELETE /users/{user_id} endpoints are perfectly RESTful for operating 
on a specific, known user. These are essential, especially if you have administrative roles.
"""
@router.put('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_existing_user(updt_user: UserUpdate, db: AsyncSession = Depends(get_db), user:User = Depends(get_current_user)) -> UserOut:
    updated_user = await update_user(user.id, updt_user, db)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user.id} not found')
    return updated_user



@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(db: AsyncSession=Depends(get_db), user:User=Depends(get_current_user)) -> None: 
    deleted_user = await delete_user(user.id, db)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user.id} not found')
    return None
