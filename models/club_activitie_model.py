from db.database import Base
from sqlalchemy import Column , Integer  , String , DateTime  , Text , ForeignKey , Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class ClubActivityModel(Base): 
    __tablename__ = "club_activities"
    id = Column(Integer , primary_key=True)

    club_id  = Column(Integer , ForeignKey("clubs.id",ondelete="CASCADE"),nullable=False)

    title = Column(String(200),nullable=False)

    description = Column(Text,nullable=True)

    assignee_id = Column(Integer,ForeignKey("users.id"),nullable=True)

    status = Column(Enum("TODO","IN_PROGRESS","DONE"),nullable=False,default="TODO")

    priority = Column(Enum("LOW", "MEDIUM", "HIGH"),nullable=False,default="MEDIUM")

    due_date = Column(DateTime,nullable=True)

    created_at = Column(DateTime ,nullable=False,default=datetime.utcnow)

    club = relationship("ClubModel",back_populates="activities") # nối đến bảng club 
    assignee = relationship("UserModel",back_populates="activities") # nối đến bảng user 