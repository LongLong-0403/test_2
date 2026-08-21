from sqlalchemy.orm import Session 
import models 
from sqlalchemy import or_ 

def get_user(db:Session , search : str |None = None , is_active : bool | None = None): 
    query = db.query(models.UserModel)
    # nếu có search thì tìm theo tên hoặc email 
    if search: 
        query = query.filter(
            or_(
                models.UserModel.full_name.contains(search), 
                models.UserModel.email.contains(search)
            ) 
        )
    # nếu có cả trạng thái 
    if is_active is not None : 
        query = query.filter(
            models.UserModel.is_active == is_active
        )

    user = query.all()

    return user 