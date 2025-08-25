from sqlalchemy import Column, Integer, String
from database import Base # type: ignore[import-not-found]


class CookBook(Base):
    __tablename__ = "Cookbook"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer, default=0)
    cook_time = Column(Integer, default=0)
    descript = Column(String)
    ingredients = Column(String, default=" ")
