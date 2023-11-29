from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    todoitem = Column(String)
    itemstatus = Column(String)
    category = Column(String)