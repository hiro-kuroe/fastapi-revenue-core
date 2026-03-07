from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.db import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.enums import SubscriptionStatus
from datetime import datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")

    if user_id is None:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Token missing subject",
         )
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="User not found"
         )
    
    return user

def require_pro_user(
        current_user: User = Depends(get_current_user)
):
    if current_user.subscription_status != SubscriptionStatus.PRO:
        raise HTTPException(status_code=403, detail="PRO required")
    
    return current_user

def require_active_subscription(
    current_user: User = Depends(get_current_user)
):
    end = current_user.current_period_end

    if end is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Subscription inactive",
        )
        
    now = datetime.now(timezone.utc)
    
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    if now >= end:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Subscription expired"
        )
    
    return current_user
          