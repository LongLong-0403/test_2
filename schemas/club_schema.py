from pydantic import BaseModel , Field , ConfigDict
from datetime import datetime

class ClubCreateRequest(BaseModel): # nhận dữ liệu khi tạo club
    name: str = Field(min_length=1 , max_length=50)
    description : str | None = None

class ClubUpdateRequest(BaseModel): # nhận dữ liệu khi thay đổi club 
    name: str | None = Field(default=None, min_length=1, max_length=50) 
    description : str | None = None

class ClubResponse(BaseModel):  # dữ liệu trả về 
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class ClubResponeDelete(BaseModel): 
    message : str 
    data : ClubResponse
# lưu ý yêu cầu create club request sẽ không có owner id vì khi người dùng đăng nhập 
# sẽ lấy theo id của user luôn 
