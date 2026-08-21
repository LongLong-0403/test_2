from db.database import Base
from sqlalchemy import Column , Integer  , String , DateTime  , Text , ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class ClubModel(Base): 
    __tablename__ = "clubs"
    id = Column(Integer , primary_key=True)

    name = Column(String(50)  , nullable= False)

    description = Column(Text,nullable=True)

    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False )

    created_at = Column(DateTime ,nullable=False,default=datetime.utcnow)

    owner = relationship("UserModel",back_populates="clubs")
    members = relationship("ClubMemberModel",back_populates="club")

    activities = relationship("ClubActivityModel",back_populates="club")