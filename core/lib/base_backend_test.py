import unittest

from core.lib.config import get_config
from core.lib.connect import connect_db

class BaseBackendTest(unittest.TestCase):

    def setUp(self):
        self.db_clients = []
        configs = get_config()
        print configs
        for db_conf_name, db_configs  in configs['databases'].iteritems():
            self.db_clients.append(connect_db('mongodb://%s:%d/%s' % (db_configs['host'], db_configs['port'],
                                                                      db_configs['database'])))

    def tearDown(self):
        print 'a'
        print self.db_clients
        for db_client in self.db_clients:
            db_client.close()