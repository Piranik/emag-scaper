import logging
import time

from rabbitmq.lib.base_consumer import BaseConsumer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

class PriceConsumer(BaseConsumer):
    def __init__(self, url):
        BaseConsumer.__init__(self, url)

    def on_message(self, unused_channel, basic_deliver, properties, body):
        print 'new msg'
        print body
        self._channel.basic_ack(basic_deliver.delivery_tag)
        time.sleep(1)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    example = PriceConsumer('amqp://guest:guest@rabbitmq:5672/%2F')
    try:
        example.run()
        print 'Am dormit'
        time.sleep(1)
        print 'Am dormit'

    except KeyboardInterrupt:
        example.stop()


if __name__ == '__main__':
    main()
