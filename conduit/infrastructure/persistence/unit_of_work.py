import contextlib
from typing import AsyncIterator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.followers import FollowersRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext
from conduit.domain.repositories.users import UsersRepository
from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.repositories.articles import (
    SQLiteArticlesRepository,
)
from conduit.infrastructure.persistence.repositories.followers import (
    SQLiteFollowersRepository,
)
from conduit.infrastructure.persistence.repositories.users import SQLiteUsersRepository
from conduit.infrastructure.time import CurrentTime

ContextFactory = Callable[[AsyncSession], UnitOfWorkContext]


class SqliteUnitOfWorkContext(UnitOfWorkContext):

    def __init__(
        self,
        session: AsyncSession,
        now: CurrentTime,
    ) -> None:
        self._users = SQLiteUsersRepository(session, now)
        self._articles = SQLiteArticlesRepository(session, now)
        self._followers = SQLiteFollowersRepository(session, now)

    @property
    def users(self) -> UsersRepository:
        return self._users

    @property
    def articles(self) -> ArticlesRepository:
        return self._articles

    @property
    def followers(self) -> FollowersRepository:
        return self._followers


def context_factory(
    now: CurrentTime,
) -> Callable[[AsyncSession], SqliteUnitOfWorkContext]:
    def inner_factory(session: AsyncSession) -> SqliteUnitOfWorkContext:
        return SqliteUnitOfWorkContext(session, now)

    return inner_factory


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
