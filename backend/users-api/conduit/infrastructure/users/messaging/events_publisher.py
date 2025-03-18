from typing import Final, final

from pika import BasicProperties
from pydantic import BaseModel

from conduit.application.users.services.events_publisher import EventsPublisher
from conduit.domain.users.events.user_created import UserCreatedEvent
from conduit.domain.users.events.user_updated import UserUpdatedEvent
from conduit.infrastructure.users.messaging.messages.user_created import (
    UserCreatedMessage,
)
from conduit.infrastructure.users.messaging.messages.user_updated import (
    UserUpdatedMessage,
)
from conduit.shared.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker

PERSISTENT_DELIVERY_MODE: Final = 2

DOMAIN_EVENTS_EXCHANGE_NAME: Final = "domain_events"
USER_CREATED_EVENT_NAME: Final = "user_created"
USER_UPDATED_EVENT_NAME: Final = "user_updated"


@final
class RabbitMQEventsPublisher(EventsPublisher):
    def __init__(self, broker: RabbitMQBroker) -> None:
        self._broker = broker

    async def user_created(self, event: UserCreatedEvent) -> None:
        message = UserCreatedMessage.from_event(event)
        await self._publish_message(USER_CREATED_EVENT_NAME, message)

    async def user_updated(self, event: UserUpdatedEvent) -> None:
        message = UserUpdatedMessage.from_event(event)
        await self._publish_message(USER_UPDATED_EVENT_NAME, message)

    async def _publish_message(self, routing_key: str, message: BaseModel) -> None:
        with self._broker.channel() as channel:
            channel.basic_publish(
                exchange="domain_events",
                routing_key=routing_key,
                body=message.model_dump_json(),
                properties=BasicProperties(
                    content_type="application/json",
                    delivery_mode=PERSISTENT_DELIVERY_MODE,
                ),
            )
