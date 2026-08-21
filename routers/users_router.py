from fastapi import APIRouter , Depends  , Query
from dependencies.auth import get_current_user
from dependencies.role import admin_required
from schemas.user_schema import UserRespone
from sqlalchemy.orm import Session 
from db.database import get_db
import models 
from schemas.user_schema import UserRespone
from services.user_service import get_user


router = APIRouter(
    prefix="/users"
    ,tags=["Users"]
)
# endpoint lấy dữ liệu cá nhân đăng nhập 
@router.get("/me",response_model=UserRespone)
def get_profile(current_user = Depends(get_current_user)): 
    return current_user

@router.get("/",response_model=list[UserRespone])
def get_all_user(search : str | None = Query(None) , is_active: bool | None = Query(default=None)
    , current_admin=Depends(admin_required) , db: Session = Depends(get_db)
    ): 
    return get_user(db=db , search= search , is_active= is_active)