from db.database import Base
from sqlalchemy import Column , Integer  , String , DateTime   , ForeignKey , Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class ClubMemberModel(Base): 
    __tablename__ = "club_members"
    club_id = Column(Integer,ForeignKey("clubs.id",ondelete="CASCADE"),primary_key=True)

    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)

    role = Column(Enum("OWNER", "MEMBER"),nullable=False,default="MEMBER")

    joined_at = Column(DateTime,nullable=False ,default=datetime.utcnow)

    user = relationship("UserModel",back_populates="members")
    club = relationship("ClubModel",back_populates="members")

