from fastapi import Depends, HTTPException

from app.deps import get_current_user


def require_role(*allowed):
    def check(user=Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(403, "Your role may not do this")
        return user

    return check
