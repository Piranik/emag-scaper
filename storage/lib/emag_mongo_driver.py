import os

from core.lib.config import get_config
from core.lib.connect import connect_db
from storage.model.product_model import Price
from storage.model.emag_product_model import EmagProduct

DB_CONFIG = 'price-db'

class EmagProductMongoDriver(object):

    def __init__(self):
        configs = get_config()['databases'][DB_CONFIG]
        url = 'mongodb://%s:%d/%s' % (configs['host'], configs['port'], configs['database'])
        connect_db(url)

    def insert_product(self, product_dict):
        product = EmagProduct(**product_dict)
        product.save()
        return product.id

    def get_products(self):
        return [product for product in EmagProduct.objects]

    def get_product(self, product_id):
        return EmagProduct.objects.get(id=product_id).to_mongo().to_dict()

    def remove_product(self, product_id):
        return EmagProduct.objects.delete(id=product_id)

    def update_product_price(self, product_id, price, day):
        product = EmagProduct.objects.get(id=product_id)
        if product:
            # Check if last price differ
            last_price = product.prices[-1]
            if last_price.value == price:
                last_price.finish_timestamp = day
            else:
                product.prices[-1].finish_timestamp = day
                product.prices.append(Price(start_timestamp=day, value=price, finish_timestamp=day))
            product.updated_at = day
            product.save()
            return True
        return False
