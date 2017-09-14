from mongoengine import connect
from core.lib.config import get_config

class PriceMongoDriver(object):
    def __init__(self):
        mongo_config = get_config()['price_mongo']
        self._connection = connect(mongo_config['db_name'], host=mongo_config['host'], port=mongo_config['port'])
        if not self._connection:
            print 'Mongo Connection Error'
        
        # aici continui cu driver-ul

