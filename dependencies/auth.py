from fastapi import HTTPException , Depends , status
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer

from sqlalchemy.orm import Session 
import jwt 

from db.database import get_db 
from core.config import SECRET_KEY , ALGORITHM 

import models

# tạo cơ chế đọc token từ beaber 
security = HTTPBearer()

# hàm lấy thông tin user từ JWT 
def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security),db : Session = Depends(get_db)): 
    # Lấy riêng từng chuỗi JWT trong token 
    # ví dụ # Authorization: Bearer abcxyz123
    # token sẽ lấy abcxyz123
    token = credentials.credentials 

    try: 
        # giải mã và kiểm tra JWT 
        # SECRET_KEY dùng để xác minh token
        # ALGORITHM phải giống thuật toán lúc tạo token
        payload = jwt.decode(token , SECRET_KEY , algorithms= [ALGORITHM])  

        # lấy user id đã lưu trong sub 
        user_id = payload.get("sub")

        # kiểm tra nếu không có sub thì không hợp lệ 
        if user_id is None : 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    # token hết hạn 
    except jwt.ExpiredSignatureError: 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail= "Token has expired"
        )
    # các trường hợp không hợp lệ  của token như bị sai , chỉnh sửa 
    except jwt.InvalidTokenError: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED , 
            detail="Invalid token"
        )
    
     # Tìm user tương ứng trong database
    user = db.query(models.UserModel).filter(models.UserModel.id == int(user_id)).first()

    # Token chứa user không còn tồn tại 
    if not user : 
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, 
            detail= "User not found"
        )
    if not user.is_active: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Account is inactive"
        )
    return user
