from sqlalchemy.future import select
from fastapi import FastAPI, Path
from contextlib import asynccontextmanager


from typing import List  

import schemas  # type: ignore[import-not-found]
import models  # type: ignore[import-not-found]
from database import engine, session  # type: ignore[import-not-found]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/recipes/", response_model=List[schemas.CookBookOut])
async def recipes() -> List[models.CookBook]:
    async with session as async_session:
        res = await async_session.execute(
            select(models.CookBook).order_by(models.CookBook.count.desc())
        )
        await async_session.commit()
    result = res.scalars().all()
    return [schemas.CookBookOut.model_validate(row) for row in result]
    

@app.get("/recipes/{recipe_id}", response_model=schemas.CookBookOut)
async def get_recipes_id(
    recipe_id: int = Path(..., title="id of recipe")
) -> models.CookBook | str:
    async with session as async_session:
        res = await async_session.execute(
            select(models.CookBook).where(recipe_id == models.CookBook.id)
        )
        if res:
            result = res.scalar()
            result.count += 1
            await async_session.commit()
        else:
            result = "[]"
        return result


@app.post("/recipes/", response_model=schemas.CookBookIn)
async def add_recipe(recipe: schemas.CookBookIn) -> schemas.CookBookIn:
    new_recipe = models.CookBook(  
        name=recipe.name, 
        descript=recipe.descript,
        cook_time=recipe.cook_time,
        ingredients=recipe.ingredients,
    )    
    async with session as async_session:        
        async_session.add(new_recipe)
        await async_session.commit()
        res = schemas.CookBookIn.model_validate(new_recipe)
    return res.model_dump()
