from typing import final

from pika import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection


@final
class RabbitMQBroker:
    def __init__(self, rabbitmq_url: str) -> None:
        url_parameters = URLParameters(rabbitmq_url)
        self._connection = BlockingConnection(url_parameters)
        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_count=1)

    def dispose(self) -> None:
        self._connection.close()

    @property
    def channel(self) -> BlockingChannel:
        return self._channel
