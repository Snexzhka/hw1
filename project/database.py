from sqlalchemy.ext.asyncio import AsyncSession  # isort:skip
from sqlalchemy.ext.asyncio import async_sessionmaker  # isort:skip
from sqlalchemy.ext.asyncio import create_async_engine  # isort:skip
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./apps.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)  # noqa: E501

Base = declarative_base()
