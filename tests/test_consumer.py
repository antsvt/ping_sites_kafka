'''
Test consumer
'''

import unittest

from src import consumer
from . import mocks

consumer.old_save_to_db = consumer.save_status_to_db
consumer.save_status_to_db = mocks.save_to_db

class ConsumerTest(unittest.TestCase):
    '''
    Test suite for consumer
    '''

    def test_create_needed_table_does_not_exist(self):
        '''
        Test table creation
        '''

        cursor = mocks.CursorMock(throw=True)
        db = mocks.ConnectionMock()
        consumer.create_status_table_if_needed(db, cursor)
        self.assertEqual(db.was_commit, True)
        self.assertTrue("CREATE TABLE" in cursor.command)


    def test_create_needed_table_exists(self):
        '''
        Test double table creation
        '''

        cursor = mocks.CursorMock()
        db = mocks.ConnectionMock()
        consumer.create_status_table_if_needed(db, cursor)
        self.assertEqual(db.was_commit, True)


    def test_run(self):
        '''
        Do general test
        '''

        consumer.connect_to_db = mocks.connect_to_db
        consumer.connect_to_kafka = mocks.connect_to_kafka
        consumer.save_status_to_db = mocks.save_to_db

        mocks.was_save = False
        consumer.run()
        self.assertEqual(mocks.was_save, True)


    def test_deserealize(self):
        '''
        Positive test for deserealization
        '''

        message = mocks.MockKafkaMessage('''{"site": "google.com",
                                 "status" : true,
                                 "elapsed": 1}''', 2)
        res = consumer.deserialize(message)
        self.assertEqual(res["site"], "google.com")
        self.assertEqual(res["status"], True)
        self.assertEqual(res["elapsed"], 1)
        self.assertEqual(res["when"], 2)


    def test_save_status_to_db(self):
        '''
        Test for saving data
        '''

        cursor = mocks.CursorMock()
        db = mocks.ConnectionMock()
        value = {"status": True,
                 "elapsed": 1,
                 "site": "google.com",
                 "when": 2}

        consumer.old_save_to_db(db, cursor, value)
        self.assertEqual(db.was_commit, True)
        self.assertTrue("INSERT INTO" in cursor.command)


if __name__ == '__main__':
    unittest.main()
    