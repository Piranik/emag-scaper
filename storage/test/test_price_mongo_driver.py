import random
import string
import time

from core.lib.base_backend_test import BaseBackendTest
from core.lib.constants.time import MONTH, WEEK
from storage.lib.helpers import get_last_price
from storage.lib.emag_mongo_driver import EmagProductMongoDriver



class TestPriceMongoDriver(BaseBackendTest):

    def setUp(self):
        super(TestPriceMongoDriver, self).setUp()
        self.price_driver = EmagProductMongoDriver()

    def test_product_insert(self):
        expected_product = getPriceFixture()
        product_id = self.price_driver.insert_product(expected_product)
        self.assertIsNotNone(product_id)
        self.assertEqual(1, len(self.price_driver.get_products()), 'More than one product was returned')
        product = self.price_driver.get_product(product_id)

    def test_update_same_price(self):
        # Insert product
        expected_product = getPriceFixture()
        product_id = self.price_driver.insert_product(expected_product)
        self.assertIsNotNone(product_id)

        # Update product with same price
        last_price = get_last_price(expected_product)
        current = int(time.time())
        updated = self.price_driver.update_product_price(product_id, last_price['value'], current)
        self.assertTrue(updated)
        expected_product['prices'][-1]['finish_timestamp'] = current
        expected_product['_id'] = product_id
        expected_product['updated_at'] = current

        # Check if last timestamp is current
        updated_product = self.price_driver.get_product(product_id)
        self.assertEqual(expected_product, updated_product, "Product was not updated correctly.")

    def test_update_new_price(self):
        # Insert product
        expected_product = getPriceFixture()
        product_id = self.price_driver.insert_product(expected_product)
        self.assertIsNotNone(product_id)

        # Update product with new price
        last_price = get_last_price(expected_product)
        current = int(time.time())
        new_price = last_price['value'] + 1
        updated = self.price_driver.update_product_price(product_id, new_price, current)
        self.assertTrue(updated)

        last_price = get_last_price(expected_product)
        last_price['finish_timestamp'] = current
        expected_product['prices'].append({'start_timestamp': last_price['finish_timestamp'], 'value': new_price,
                                                'finish_timestamp': current})
        expected_product['_id'] = product_id
        expected_product['updated_at'] = current

        # Check if last timestamp is current
        updated_product = self.price_driver.get_product(product_id)
        self.assertEqual(expected_product, updated_product, "Product was not updated correctly.")

    def tearDown(self):
        super(TestPriceMongoDriver, self).tearDown()


def getPriceFixture():
    current = int(time.time())
    start_date = int(current - MONTH)
    emag_prices = [{'start_timestamp': period-WEEK, 'value': random.random()*1000, 'finish_timestamp': period} for
                   period in range(start_date, current, WEEK)]
    return {
        'product_id': generate_random_string(10),
        'category': generate_random_string(10),
        'name': generate_random_string(20),
        'link': generate_random_string(10),
        'created_at': current-MONTH,
        'updated_at': current,
        'prices': emag_prices
    }

def generate_random_string(length):
    return ''.join([random.choice(string.ascii_uppercase) for _ in range(length)])