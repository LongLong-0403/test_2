import bcrypt 
import jwt 
from datetime import datetime , timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES , SECRET_KEY , ALGORITHM
def hash_password(password : str) -> str:  # băm mật khẩu kkkk 
    salt = bcrypt.gensalt()

    hased = bcrypt.hashpw(password.encode(),salt)

    return hased.decode()


# hàm kiểm tra mật khẩu khi đăng nhập 
def verify_password(password : str , hash_password: str) -> bool : 
    return bcrypt.checkpw(password.encode() , hash_password.encode())



# tạo token 
def create_access_token(data:dict) -> str : 
    # lấy dữ liệu 
    payload = data.copy()

    # tính thời gian tồn tại của token 
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)

    # update 
    payload.update({
        "exp":expire
    })
    # chuyển hóa token 
    token = jwt.encode(
        payload ,SECRET_KEY , algorithm=ALGORITHM
    )
    return token