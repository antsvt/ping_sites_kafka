'''
Test producer
'''

import time
import unittest
import threading

from src import producer
from . import mocks

from config import Config
from handler import Handler


def stop_thread_function(_: str):
    '''
    Notify about exit
    '''
    time.sleep(1)
    Handler.should_exit = True

producer.connect_to_kafka = mocks.connect_to_kafka
producer.check_site = mocks.check_site
producer.send_message = mocks.send_message


class ProducerTest(unittest.TestCase):
    '''
     Test suite for the producer
    '''

    def test_run(self):
        '''
        Do tests
        '''
        Config.interval_between_checks_in_sec = 0
        mocks.last_checked_site = False
        mocks.was_send_message = False

        x = threading.Thread(target=stop_thread_function, args=(1,))
        x.start()

        producer.run()

        self.assertEqual(mocks.was_send_message, True)
        self.assertEqual(mocks.last_checked_site,
                        'https://www.nonexistentwebsite.com')


if __name__ == '__main__':
    unittest.main()
