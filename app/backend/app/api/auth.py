from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from app.core.config import settings
from app.core.audit_helper import log_audit_event
from app.models.user import User
from app.schemas.user import Token, TokenRefreshRequest, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        or_(User.username == form_data.username, User.email == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    role_val = user.role.value if hasattr(user.role, "value") else str(user.role)
    token_data = {"sub": user.username, "role": role_val, "user_id": user.user_id}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data=token_data)

    log_audit_event(
        db=db,
        user_id=user.user_id,
        action="LOGIN",
        module="AUTH",
        description=f"User '{user.username}' successfully logged in."
    )
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user)
    }


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    payload: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    token_payload = verify_refresh_token(payload.refresh_token)
    username = token_payload.get("sub")

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or account deactivated"
        )

    role_val = user.role.value if hasattr(user.role, "value") else str(user.role)
    token_data = {"sub": user.username, "role": role_val, "user_id": user.user_id}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    new_refresh_token = create_refresh_token(data=token_data)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user)
    }