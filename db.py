from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import  Column, Integer, String, DateTime


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    pass

class History(Base):
    __tablename__ = "history"
 
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    request = Column(String)
    response = Column(String)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()