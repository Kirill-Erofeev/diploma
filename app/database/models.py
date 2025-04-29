from sqlalchemy import  Column, Integer, String, DateTime
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

class History(Base):
    __tablename__ = "history"
 
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    request = Column(String)
    response = Column(String)
    username = Column(String)