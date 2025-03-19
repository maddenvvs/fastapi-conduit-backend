import asyncio
import uuid
from threading import Thread
from typing import Any, Final, final

from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import (
    AMQPChannelError,
    AMQPConnectionError,
    ConnectionClosedByBroker,
)
from sqlalchemy import insert, update
from typing_extensions import override

from conduit.infrastructure.messaging.messages.user_created import UserCreatedMessage
from conduit.infrastructure.messaging.messages.user_updated import UserUpdatedMessage
from conduit.infrastructure.persistence.models import UserModel
from conduit.shared.application.unit_of_work import UnitOfWorkFactory
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
from conduit.shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork

RABBITMQ_LISTENER_THREAD_NAME: Final = "RabbitMQ Domain Event Listener Thread"


@final
class RabbitMQEventsSubscriber(Thread):
    def __init__(
        self,
        message_broker: RabbitMQBroker,
        uow_factory: UnitOfWorkFactory,
        now: CurrentTime,
    ) -> None:
        super().__init__(name=RABBITMQ_LISTENER_THREAD_NAME, daemon=True)

        self._message_broker = message_broker
        self._uow_factory = uow_factory
        self._now = now

        self._event_loop = asyncio.new_event_loop()

    def _on_user_created(
        self,
        channel: BlockingChannel,
        method_frame: Any,
        header_frame: Any,
        body: Any,
    ) -> None:
        del header_frame

        message = UserCreatedMessage.model_validate_json(body)
        self._event_loop.run_until_complete(self._create_user(message))

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    async def _create_user(self, message: UserCreatedMessage) -> None:
        async with self._uow_factory():
            session = SqlAlchemyUnitOfWork.get_current_session()
            current_time = self._now()
            user_id = uuid.UUID(message.user_id)

            query = insert(UserModel).values(
                user_id=user_id,
                username=message.username,
                bio=message.bio,
                image_url=message.image_url,
                created_at=current_time,
                updated_at=current_time,
            )
            await session.execute(query)

    def _on_user_updated(
        self,
        channel: BlockingChannel,
        method_frame: Any,
        header_frame: Any,
        body: Any,
    ) -> None:
        del header_frame

        message = UserUpdatedMessage.model_validate_json(body)
        self._event_loop.run_until_complete(self._update_user(message))

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    async def _update_user(self, message: UserUpdatedMessage) -> None:
        async with self._uow_factory():
            session = SqlAlchemyUnitOfWork.get_current_session()
            current_time = self._now()
            user_id = uuid.UUID(message.user_id)

            query = (
                update(UserModel)
                .where(UserModel.user_id == user_id)
                .values(
                    username=message.username,
                    bio=message.bio,
                    image_url=message.image_url,
                    updated_at=current_time,
                )
            )
            await session.execute(query)

    @override
    def run(self) -> None:
        while True:
            try:
                with self._message_broker.channel() as channel:
                    channel.basic_qos(prefetch_count=1)
                    channel.basic_consume(
                        queue="user_created",
                        on_message_callback=self._on_user_created,
                    )
                    channel.basic_consume(
                        queue="user_updated",
                        on_message_callback=self._on_user_updated,
                    )
                    channel.start_consuming()
                    channel.stop_consuming()
            except ConnectionClosedByBroker:  # noqa: PERF203
                continue
            # Do not recover on channel errors
            except AMQPChannelError:
                continue
            # Recover on all other connection errors
            except AMQPConnectionError:
                continue
