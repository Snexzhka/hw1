
from contextlib import asynccontextmanager

import models
import schemas
from typing import List
from database import engine, session

from sqlalchemy.future import select
from fastapi import FastAPI, Path




@asynccontextmanager
async def lifespan(app:FastAPI):
    async  with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)



@app.get('/recipes/', response_model=List[schemas.CookBookOut])
async def recipes() -> List[models.CookBook]:
    async with session as async_session:
        res = await async_session.execute(select(models.CookBook).order_by(models.CookBook.count.desc()))
        await async_session.commit()
    return res.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.CookBookOut)
async  def get_recipes_id(recipe_id: int = Path(...,title="id of recipe"))-> models.CookBook | str:
    async  with session as async_session:
        res = await async_session.execute(
                select(models.CookBook).where(recipe_id == models.CookBook.id))

        if res:
            result = res.scalar()
            result.count += 1
            await async_session.commit()
        else:
            result = "[]"
        return result



@app.post("/recipes/", response_model=schemas.CookBookOut)
async def add_recipe(recipe: schemas.CookBookIn)-> models.CookBook:
    new_recipe = models.CookBook(name=recipe.name, cook_time=recipe.cook_time,
                                 descript=recipe.descript, ingredients=recipe.ingredients)
    async with session.begin():
        session.add(new_recipe)
        session.commit()
        return new_recipe


