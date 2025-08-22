from database import Base
from sqlalchemy import Column, String, Integer


class CookBook(Base):
    __tablename__ = "Cookbook"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    count = Column(Integer, index=True, default=0)
    cook_time = Column(Integer, index=True,  default=0)
    descript = Column(String)
    ingredients = Column(String, default=" ")

