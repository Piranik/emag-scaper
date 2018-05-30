import logging
import time

from rabbitmq.lib.base_consumer import BaseConsumer
from product_actions import ProductActions
class PriceConsumer(BaseConsumer):
    def __init__(self, url):
        BaseConsumer.__init__(self, url)
        QUEUE_NAME = 'product-writer-processor'


    def on_message(self, unused_channel, basic_deliver, properties, message):
        self._channel.basic_ack(basic_deliver.delivery_tag)
        print 'new msg'
        print message
        action = message[ProductActions.ACTION_FIELD]
        if action == ProductActions.INSERT:
            self._insert_handler(message)
        elif action == ProductActions.UPDATE:
            self._update_handler(message)
        else:
            print 'no action on message: %r' % message

    def _insert_handler(self, message):
        pass

    def _update_handler(self, message):
        pass



