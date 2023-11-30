from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    taskname = Column(String)
    taskstatus = str = "open"
    taskcategory = Column(String)