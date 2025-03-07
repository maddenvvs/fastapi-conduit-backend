import abc
from contextvars import ContextVar, Token
from types import TracebackType
from typing import Optional, final

from typing_extensions import Self

# Was taken from here:
# https://dev.to/luscasleo/using-pythons-contextvars-api-1iec


@final
class ContextTokenAlreadyExistsError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("Already have a current context token", *args)


@final
class NoCurrentContextTokenError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("No current context token", *args)


@final
class NoContextSessionError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("No context session", *args)


class UnitOfWork(abc.ABC):
    _current_context_token: Optional[Token[Optional["UnitOfWork"]]] = None

    def set_current_context(self) -> None:
        if self._current_context_token is not None:
            raise ContextTokenAlreadyExistsError

        self._current_context_token = _current_unit_of_work.set(self)

    def remove_current_context(self) -> None:
        if self._current_context_token is None:
            raise NoCurrentContextTokenError

        _current_unit_of_work.reset(self._current_context_token)

    @staticmethod
    def get_current_context() -> "UnitOfWork":
        context = _current_unit_of_work.get()
        if context is None:
            raise NoContextSessionError
        return context

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...

    @abc.abstractmethod
    async def close(self) -> None: ...

    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]: ...


_current_unit_of_work: ContextVar[Optional[UnitOfWork]] = ContextVar(
    "current_unit_of_work",
    default=None,
)


class UnitOfWorkFactory(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> UnitOfWork: ...
