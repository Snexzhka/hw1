from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import update
from sqlalchemy.future import select

import models  # type: ignore[import-not-found]
import schemas  # type: ignore[import-not-found]
from database import async_session, engine  # type: ignore[import-not-found]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/recipes/", response_model=List[schemas.CookBookOut])
async def recipes() -> List[schemas.CookBookOut]:
    async with async_session() as session:

        res = await session.execute(
            select(models.CookBook).order_by(models.CookBook.count.desc())
        )
        await session.commit()
    result = res.scalars().all()
    return [schemas.CookBookOut.model_validate(row) for row in result]


@app.get("/recipes/{recipe_id}", response_model=schemas.CookBookOut)
async def get_recipes_id(
    recipe_id: int = Path(..., title="id of recipe")
) -> schemas.CookBookOut | dict:
    async with async_session() as session:
        query = select(models.CookBook).where(models.CookBook.id == recipe_id)
        res = await session.execute(query)
        result = res.scalar()
        if result:
            query_for_count = (
                update(models.CookBook)
                .where(models.CookBook.id == recipe_id)
                .values(count=result.count + 1)
            )
            await session.execute(query_for_count)
            await session.commit()
            answer: schemas.CookBookOut | dict = schemas.CookBookOut.model_validate(
                result
            )
            return answer
        raise HTTPException(status_code=404, detail="not found")


@app.post("/recipes/", response_model=schemas.CookBookIn)
async def add_recipe(recipe: schemas.CookBookIn) -> schemas.CookBookIn:
    new_recipe = models.CookBook(
        name=recipe.name,
        descript=recipe.descript,
        cook_time=recipe.cook_time,
        ingredients=recipe.ingredients,
    )
    async with async_session() as session:
        session.add(new_recipe)
        await session.flush()
        await session.commit()
        return schemas.CookBookIn.model_validate(new_recipe)
        # print("res", res)
        # return res.model_dump()
