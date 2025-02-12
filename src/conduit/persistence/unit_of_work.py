import contextlib
from typing import AsyncIterator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext
from conduit.domain.repositories.users import UsersRepository
from conduit.persistence.database import Database
from conduit.persistence.repositories.tags import SQLiteTagsRepository
from conduit.persistence.repositories.users import SQLiteUsersRepository
from conduit.time import CurrentTime

ContextFactory = Callable[[AsyncSession], UnitOfWorkContext]


def context_factory(now: CurrentTime):
    def inner_factory(session: AsyncSession):
        return SqliteUnitOfWorkContext(session, now)

    return inner_factory


class SqliteUnitOfWorkContext(UnitOfWorkContext):

    def __init__(
        self,
        session: AsyncSession,
        now: CurrentTime,
    ) -> None:
        self._tags = SQLiteTagsRepository(session)
        self._users = SQLiteUsersRepository(session, now)

    @property
    def tags(self) -> ITagsRepository:
        return self._tags

    @property
    def users(self) -> UsersRepository:
        return self._users


class SqliteUnitOfWork(UnitOfWork):

    def __init__(
        self,
        db: Database,
        context_factory: ContextFactory,
    ):
        self._db = db
        self._context_factory = context_factory

    @contextlib.asynccontextmanager
    async def begin(self) -> AsyncIterator[UnitOfWorkContext]:
        async with self._db.session() as session:
            yield self._context_factory(session)
