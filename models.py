from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class Item(BaseModel):
    name: str
    price: float
    description: str = None

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), index=True, nullable=False)

