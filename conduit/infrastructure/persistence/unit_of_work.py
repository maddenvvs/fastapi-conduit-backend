from types import TracebackType
from typing import Optional, final

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Self

from conduit.domain.unit_of_work import UnitOfWork, UnitOfWorkFactory
from conduit.infrastructure.persistence.database import Database


@final
class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._session: Optional[AsyncSession] = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("No session")

        return self._session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()

    async def __aenter__(self) -> Self:
        self.set_current_context()
        self._session = self._db.create_session()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.remove_current_context()

        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await self.close()

        if exc_type is not None and exc_value is not None:
            raise exc_value.with_traceback(traceback)

        return None

    @staticmethod
    def get_current_unit_of_work() -> "SqlAlchemyUnitOfWork":
        context = UnitOfWork.get_current_context()
        if not isinstance(context, SqlAlchemyUnitOfWork):
            raise RuntimeError("Context session is not of type 'SqlAlchemyUnitOfWork'")
        return context

    @staticmethod
    def get_current_session() -> AsyncSession:
        return SqlAlchemyUnitOfWork.get_current_unit_of_work().session


@final
class SqlAlchemyUnitOfWorkFactory(UnitOfWorkFactory):
    def __init__(self, db: Database) -> None:
        self._db = db

    def __call__(self) -> UnitOfWork:
        return SqlAlchemyUnitOfWork(self._db)
