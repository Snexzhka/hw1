from database import Base
from sqlalchemy import Column, String, Integer, Index


class CookBook(Base):
    __tablename__ = "Cookbook"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    count = Column(Integer, index=True, default=0)
    cook_time = Column(Integer, index=True,  default=0)
    descript = Column(String)
    ingredients = Column(String, default=" ")
    Index("ix_Cookbook_cook_time", "cook_time")

