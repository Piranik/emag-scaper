import logging
import pika
import json

LOGGER = logging.getLogger(__name__)


class BasePublisher(object):
    """This is a publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.
    """
    EXCHANGE = 'message'
    EXCHANGE_TYPE = 'topic'
    QUEUE = 'text'
    ROUTING_KEY = 'example.text'

    def __init__(self, amqp_url):
        self._connection = None
        self._channel = None
        self._connection_params = pika.URLParameters(amqp_url)

    def connect(self):
        self._connection = pika.BlockingConnection(self._connection_params)
        self._channel = self._connection.channel()

    def close(self):
        self._connection.close()

    def _publish_message(self, message):
        self._channel.basic_publish(self.EXCHANGE,
                                    self.ROUTING_KEY,
                                    'message',
                                    pika.BasicProperties(content_type='text/plain',
                                                         delivery_mode=1))

    def publish_message(self, message):
        raise NotImplementedError