from sqlalchemy.orm import Session 
import models 
from fastapi import HTTPException , status 
from core.security import hash_password , verify_password , create_access_token
from core.exceptions import bad_request , anauthorize , forbidden
from schemas.user_schema import UserCreateRequest  , LoginRequest

# đăng ký tài khoản người dùng
def register_user(request : UserCreateRequest , db : Session ): 
    user_db = db.query(models.UserModel).filter(models.UserModel.email == request.email).first()

    if user_db :
        bad_request("Email already exists")
    hashed_password = hash_password(request.password)

    new_user = models.UserModel(
        email = request.email , 
        password_hash = hashed_password , 
        full_name = request.full_name,
        role = "USER" , 
        is_active=True 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# đăng nhập tài khoản 
def login_user(request :LoginRequest , db: Session): 
    # tìm user theo email 
    user = db.query(models.UserModel).filter(models.UserModel.email == request.email).first()
    # no tìm thấy user 
    if not user : 
        raise HTTPException(
            status_code=  status.HTTP_401_UNAUTHORIZED, 
            detail= "Email or password is incorrect"
        )
    # kiểm tra mật khẩu 
    if not verify_password(request.password,user.password_hash): 
        anauthorize("Email or password is incorrect")
        
    # kiểm tra xem tài khoản còn hoạt động không 
    if not user.is_active: 
        forbidden("Account is inactive")
    # Tạo JWT 
    access_token = create_access_token({"sub":str(user.id)})
    return {
        "access_token" : access_token, 
        "token_type" : "bearer"
    }