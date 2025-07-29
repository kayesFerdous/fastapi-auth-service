from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import get_user_by_email
from security.hashing import verify_password
from security.token import create_access_token

async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await get_user_by_email(email=form_data.username, db=db)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}