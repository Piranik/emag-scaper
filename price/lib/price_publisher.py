import logging

from rabbitmq.lib.base_publisher import BasePublisher

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')

class PricePublisher(BasePublisher):
    def __init__(self, connection_url):
        BasePublisher.__init__(self, connection_url)

    def publish_message(self, message):
        self._publish_message(message)


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    example = PricePublisher('amqp://guest:guest@rabbitmq:5672/%2F?connection_attempts=3&heartbeat_interval=3600')
    example.connect()

    print 'Sending messages'
    for i in range(10):
        example.publish_message("message %d" % i)

if __name__ == '__main__':
    main()