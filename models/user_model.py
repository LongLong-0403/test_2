from db.database import Base
from sqlalchemy import Column , Integer , Boolean , String , DateTime , Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class UserModel(Base): 
    __tablename__ = "users"
    id = Column(Integer , primary_key=True)

    email = Column(String(50) ,unique=True , nullable= False)

    password_hash = Column(String(255) ,nullable=False)

    full_name = Column(String(100),nullable=False)

    role = Column(Enum("USER","ADMIN"),nullable=False,default="USER")

    is_active  = Column(Boolean , nullable=False,default=True)

    created_at = Column(DateTime ,nullable=False,default=datetime.utcnow)

    clubs = relationship("ClubModel",back_populates="owner") # nối đến bảng club 
    members = relationship("ClubMemberModel",back_populates="user") # nối đến bảng club member 
    activities = relationship("ClubActivityModel",back_populates="assignee")