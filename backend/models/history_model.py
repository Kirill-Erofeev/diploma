from sqlalchemy import  Column, Integer, String, DateTime

from backend.db.database import Base

class History(Base):
    __tablename__ = "history"
 
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    request = Column(String)
    response = Column(String)
    username = Column(String)