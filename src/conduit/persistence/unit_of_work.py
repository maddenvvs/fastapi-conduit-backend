import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext
from conduit.persistence.database import Database
from conduit.persistence.repositories.tags import SQLiteTagsRepository


class SqliteUnitOfWorkContext(UnitOfWorkContext):

    def __init__(self, session: AsyncSession) -> None:
        self._tags = SQLiteTagsRepository(session)

    @property
    def tags(self) -> ITagsRepository:
        return self._tags


class SqliteUnitOfWork(UnitOfWork):

    def __init__(self, db: Database):
        self._db = db

    @contextlib.asynccontextmanager
    async def begin(self) -> AsyncIterator[UnitOfWorkContext]:
        async with self._db.session() as session:
            yield SqliteUnitOfWorkContext(session)
