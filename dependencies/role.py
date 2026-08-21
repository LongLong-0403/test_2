from fastapi import Depends , status, HTTPException 
from dependencies.auth import get_current_user 

def admin_required(current_user = Depends(get_current_user)): 
    if current_user.role != "ADMIN" : 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin permission required"
        )
    return current_user