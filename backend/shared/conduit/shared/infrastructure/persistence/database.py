import contextlib
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_THERSHOLD_SIZE: Final = 100


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(
            db_url,
            echo=True,
        )

        # If I want to EXPLICITLY start any transaction,
        # "autobegin=False" can be passed to session maker factory.
        self._session = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            close_resets_only=False,
        )

    async def database_exists(self) -> bool:
        database = self._engine.url.database
        if database is None:
            return True
        if database == ":memory:":
            return False

        database_file = Path(database)
        if (
            not database_file.is_file()
            or database_file.stat().st_size < DATABASE_THERSHOLD_SIZE
        ):
            return False

        with database_file.open("rb") as f:  # noqa: ASYNC230
            header = f.read(100)

        return header[:16] == b"SQLite format 3\x00"

    async def create_tables(self, model_type: type[DeclarativeBase]) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model_type.metadata.create_all)

    async def drop_tables(self, model_type: type[DeclarativeBase]) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model_type.metadata.drop_all)

    async def create_database(self, model_type: type[DeclarativeBase]) -> None:
        if await self.database_exists():
            return

        await self.create_tables(model_type)

    async def dispose(self) -> None:
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def create_session(self) -> AsyncSession:
        return self._session()
