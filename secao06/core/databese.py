from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from core.configs import settings

engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    pool_size=10,        # Quantas conexões "garantidas" ficam abertas
    max_overflow=20,     # Quantas conexões extras podem ser abertas em picos
    pool_timeout=30,     # Quanto tempo esperar por uma conexão antes de dar erro
    pool_pre_ping=True   # Verifica se a conexão ainda está viva antes de usar (essencial!)
)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

