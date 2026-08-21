from sqlalchemy.orm import Session 
import models 
from schemas.club_schema import ClubCreateRequest , ClubUpdateRequest
from fastapi import HTTPException , status
from core.exceptions import forbidden
# tạo mới club 
def create_club(request : ClubCreateRequest , db:Session , current_user): 
    new_club = models.ClubModel(
        name  = request.name , 
        description = request.description , 
        owner_id = current_user.id 

    )

    db.add(new_club)
    # đẩy dữ liệu suống DB tạm thời để lấy new_club id 
    # nhưng sẽ phải chưa commit nhe 
    db.flush()

    new_member = models.ClubMemberModel(
        club_id = new_club.id , 
        user_id = current_user.id , 
        role = "OWNER"
    )

    db.add(new_member) 
    db.commit()
    db.refresh(new_member)

    return new_club

# lấy dữ liệu các câu lạc bộ 
def get_my_clubs(current_user , db:Session , search : str | None = None ): 
    query = db.query(models.ClubModel)

    query = query.join(
        models.ClubMemberModel, 
        models.ClubMemberModel.club_id == models.ClubModel.id
    ).filter(models.ClubMemberModel.user_id == current_user.id)
     # sử dụng join để nối dữ liệu 2 bảng nhằm lấy user_id để tìm kiếm 
    if search: 
        query = query.filter(models.ClubModel.name.contains(search))

    clubs = query.all()
    return clubs

# lấy dữ liệu câu lạc bộ theo club id và chỉ có owner / member mới được xem 
def get_club_by_id(club_id : int , db : Session , current_user ): 
    # tìm club theo id 
    club = db.query(models.ClubModel).filter(models.ClubModel.id == club_id).first()

    # kiểm tra tồn tại 
    if not club : 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Not found club "
        )
    # nếu tìm thấy kiểm tra xem có phải thành viên câu lại bộ hay không 
    member = db.query(models.ClubMemberModel).filter(
        models.ClubMemberModel.club_id == club_id , 
        models.ClubMemberModel.user_id == current_user.id 
    ).first()

    # nếu không thuộc club 
    if not member: 
        forbidden("U Not a member of this club")
    return club

#cập nhật và xóa dữ liệu chỉ owner mới được phép 

# hàm chỉ lấy danh tính owner 
def check_club_owner(club_id : int , current_user , db : Session): 
    # tìm membership của user trong club 
    member = db.query(models.ClubMemberModel).filter(
        models.ClubMemberModel.user_id == current_user.id , 
        models.ClubMemberModel.club_id == club_id

    ).first()

    # kiểm tra xem có thuộc club nào ko 
    if not member : 
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN , 
            detail="You are not a member this for club"
        )

    # kiểm tra xem có phải owner ko 
    if member.role != "OWNER": 
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN , 
            detail= "U not Owner"
        )
    return member 


# hàm sửa dữ liệu nhen  
def update_club_data(club_id : int , request : ClubUpdateRequest ,current_user ,  db : Session ): 
    # tìm kiếm câu lạc bộ 
    club = db.query(models.ClubModel).filter(models.ClubModel.id == club_id).first()

    if not club : 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND , 
            detail= "Club not found"
        )
    # kiểm tra quyền trong clb xem có phải owner ko 
    check_club_owner(club_id=club_id , current_user= current_user , db= db)

    # chỉ lấy những trường thực sự client gửi lên 
    data_update = request.model_dump(exclude_unset=True)

    # cập nhật 
    for fiel , value in data_update.items(): 
        setattr(club , fiel , value)

    db.commit()
    db.refresh(club)

    return club

# hàm xóa chỉ owner nhen 
def delete_club_data(
    club_id: int,
    current_user,
    db: Session
):
    club = db.query(models.ClubModel).filter(
        models.ClubModel.id == club_id
    ).first()

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    check_club_owner(
        club_id=club_id,
        current_user=current_user,
        db=db
    )

    
    deleted_club = {
        "id": club.id,
        "name": club.name,
        "description": club.description,
        "owner_id": club.owner_id,
        "created_at": club.created_at
    }

  
    db.delete(club)
    db.commit()

    return deleted_club


    