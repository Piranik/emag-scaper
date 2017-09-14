import sys
from core.lib.config import get_config
from storage.model.product_model import Test
from storage.lib.connect import connect_db
import time

DB_CONFIG = 'price-db'

class PriceMongoDriver(object):
    def __init__(self):
        configs = get_config()[DB_CONFIG]
        url = 'mongodb://%s:%d/%s' % (configs['host'], configs['port'], configs['database'])
        connect_db(url)
        # aici continui cu driver-ul

if __name__ == '__main__':
    print PriceMongoDriver()

    print id(PriceMongoDriver())
    print id(PriceMongoDriver())
    Test("ana").save()