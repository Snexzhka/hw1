from typing import Any, AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from .project import models
from .project.main import app
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./apps.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)

data_post = {
    "name": "Test omlet",
    "cook_time": "10",
    "descript": "for breakfast",
    "ingredients": "milk, eags",
}


@pytest_asyncio.fixture
async def setup_db():
    """
    Функция по созданию\удалению БД и передаче в нее словарика. Сначала создается база, в нее добавляется
    словарик и управление передается далее клиенту. после выполнения теста база удаляется.
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await conn.execute(insert(models.CookBook), data_post)
        await conn.commit()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(setup_db) -> AsyncGenerator[AsyncClient, Any]:
    """
    Функция по подключению клиента. В ней содержится фикстура по созданию БД (т.е. сначала создается БД,
    потом создается подключение, которое передается в тест.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def test_recipe(client):
    """
    Функция по добавлению словарика в базу. Фактически она здесь нее нужна, она нужна там, где в функции setup_db
    нет кода по передаче в базу словарика. Но я ее использовала, чтоб создать вторую запись в базе.
    """
    response = await client.post("/recipes/", json=data_post)
    return response.json()
