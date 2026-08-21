from fastapi import APIRouter , status , Depends
from db.database import get_db 
from schemas.user_schema import UserCreateRequest , UserRespone , LoginRespone , LoginRequest
from sqlalchemy.orm import Session
from services.auth_service import register_user , login_user
router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserRespone ,status_code=status.HTTP_201_CREATED)
def register(request : UserCreateRequest , db : Session = Depends(get_db)): 
    return register_user(request=request , db=db)

@router.post("/login",response_model=LoginRespone ,status_code=status.HTTP_201_CREATED)
def login(request:LoginRequest , db : Session = Depends(get_db)): 
    return login_user(request=request , db= db)