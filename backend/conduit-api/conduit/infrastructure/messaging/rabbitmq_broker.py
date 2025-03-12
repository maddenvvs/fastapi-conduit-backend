import contextlib
from collections.abc import Generator
from typing import final

from pika import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection


@final
class RabbitMQBroker:
    def __init__(self, rabbitmq_url: str) -> None:
        self._url_parameters = URLParameters(rabbitmq_url)

    @contextlib.contextmanager
    def connection(self) -> Generator[BlockingConnection]:
        connection = BlockingConnection(self._url_parameters)
        yield connection
        connection.close()

    @contextlib.contextmanager
    def channel(self) -> Generator[BlockingChannel]:
        with self.connection() as connection:
            channel = connection.channel()
            yield channel
            channel.close()
