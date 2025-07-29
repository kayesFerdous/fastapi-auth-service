from fastapi import Depends, HTTPException, status
from schemas.users import User, UserRole
from security.token import get_current_user


def admin_required(user:User=Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return user
