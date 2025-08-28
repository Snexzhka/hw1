from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Path
from sqlalchemy.future import select, update

from project import models  # type: ignore[import-not-found]
from project import schemas  # type: ignore[import-not-found]
from project.database import engine, session  # type: ignore[import-not-found]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/recipes/", response_model=List[schemas.CookBookOut])
async def recipes() -> List[schemas.CookBookOut]:
    async with asyn_session as session:
        res = await session.execute(
            select(models.CookBook).order_by(models.CookBook.count.desc())
        )
        await session.commit()
    result = res.scalars().all()
    return [schemas.CookBookOut.model_validate(row) for row in result]


@app.get("/recipes/{recipe_id}", response_model=schemas.CookBookOut)
async def get_recipes_id(
    recipe_id: int = Path(..., title="id of recipe")
) -> schemas.CookBookOut | None:
    async with async_session as session:
        res = await session.execute(
            select(models.CookBook).where(recipe_id == models.CookBook.id)
        )
        result = res.scalar()
        if result:
            result.count = result.count + 1
            print(res.count)
            res.count += 1

            await session.commit()
            return schemas.CookBookOut.model_validate(result)
       



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
     
