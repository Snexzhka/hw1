
from pydantic import BaseModel, Field, ConfigDict


# class Ingredients(BaseModel):
#     name: str=Field(..., title="name of ingr")
#     quantity: int=Field(..., title="quantity of ingred")
#     cookbook_id: int

class BaseRecipes(BaseModel):
    name: str=Field(..., title="name")
    cook_time: int=Field(..., title="time of cook")
    ingredients: str = Field(..., title="ingredients")
    descript: str = Field(..., title="description")




class CookBookIn(BaseRecipes):
    ...



    class Config:
        model_config = ConfigDict(from_attributes=True)
        from_attributes = True
        orm_mode=True

class CookBookOut(BaseRecipes):
    id: int
    count: int


    class Config:
        model_config = ConfigDict(from_attributes=True)
        from_attributes = True
        orm_mode = True


