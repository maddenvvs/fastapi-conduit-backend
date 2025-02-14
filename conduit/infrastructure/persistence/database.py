import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from conduit.infrastructure.persistence.models import Base


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(
            db_url,
            echo=True,
        )
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def create_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
