import abc

from conduit.domain.users.events.user_created import UserCreatedEvent
from conduit.domain.users.events.user_updated import UserUpdatedEvent


class EventsPublisher(abc.ABC):
    @abc.abstractmethod
    async def user_created(self, event: UserCreatedEvent) -> None: ...

    @abc.abstractmethod
    async def user_updated(self, event: UserUpdatedEvent) -> None: ...
