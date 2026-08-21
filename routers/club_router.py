from fastapi import APIRouter , Depends , HTTPException , status 
from db.database import get_db 
from dependencies.auth import get_current_user
from schemas.club_schema import ClubCreateRequest , ClubResponse , ClubUpdateRequest , ClubResponeDelete
from sqlalchemy.orm import Session 
from services.club_service import create_club , get_my_clubs , get_club_by_id , update_club_data , delete_club_data

router = APIRouter(
    prefix="/clubs", 
    tags=["Clubs"]
)

# endpont tạo câu lạc bộ và thêm member vào bẳng club member 
@router.post("/",response_model=ClubResponse ,status_code=status.HTTP_201_CREATED)
def create_new_club(request:ClubCreateRequest , db : Session = Depends(get_db) , current_user = Depends(get_current_user)): 
    return create_club(request=request , db=db , current_user=current_user)

#endpoint dùng để lấy danh sách câu lạc bộ 
@router.get("/",response_model=list[ClubResponse],status_code=status.HTTP_200_OK)
def get_clubs(search : str | None = None , current_user = Depends(get_current_user) , db : Session = Depends(get_db)): 
    return get_my_clubs(current_user=current_user , db= db , search=search)

#endpont tìm kiếm câu lạc bộ và chỉ thành viên câu lạc bộ mới được xem 
@router.get("/{club_id}",response_model=ClubResponse,status_code=status.HTTP_200_OK)
def get_club_id(club_id : int , current_user = Depends(get_current_user) , db:Session = Depends(get_db)): 
    return get_club_by_id(club_id=club_id , db= db , current_user= current_user)

#endpoint sửa dữ liệu Sử dụng PATCH  chỉ owner 
@router.patch("/{club_id}",response_model=ClubUpdateRequest , status_code=status.HTTP_200_OK)
def update_club(club_id : int ,  request : ClubUpdateRequest, current_user = Depends(get_current_user), db : Session = Depends(get_db)) : 
    return update_club_data(club_id=club_id , request=request , current_user=current_user , db=db)

#endpoint xóa dữ liệu sử dụng DELETE chỉ owner 
@router.delete("/{club_id}",response_model=ClubResponeDelete , status_code= status.HTTP_200_OK)
def delete_club(club_id : int , current_user = Depends(get_current_user),db : Session = Depends(get_db)): 
    return {
        "message" : "Xóa thành công", 
        "data": delete_club_data(club_id= club_id , current_user= current_user , db= db)
    }

