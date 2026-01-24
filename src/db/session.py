from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from src.config.settings import settings

db_params = {}
if settings.MODE == "TEST":
    db_params = {"poolclass": NullPool}

engine = create_async_engine(settings.DATABASE_URL, **db_params)
engine_null_pool = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
AsyncSessionLocalNullPool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)
