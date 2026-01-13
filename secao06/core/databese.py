from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from core.configs import settings
from typing import Any

engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True
)
session_factory: Any = sessionmaker

Session = session_factory(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
