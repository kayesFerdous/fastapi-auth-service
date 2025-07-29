from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service import login_for_access_token
from database import get_db
from schemas.users import User
from schemas.auths import Token
from security.token import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_for_access_token(form_data, db)


@router.get('/user_active', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user