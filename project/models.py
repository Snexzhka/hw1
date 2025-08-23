from sqlalchemy import Column, String, Integer
from database import Base  # type: ignore[import-not-found]
# mypy: enable-error-code="truthy-bool, ignore-without-code"



class CookBook(Base):
    __tablename__ = "Cookbook"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer, default=0)
    cook_time = Column(Integer, default=0)
    descript = Column(String)
    ingredients = Column(String, default=" ")
    
