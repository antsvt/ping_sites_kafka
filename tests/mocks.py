'''
Mocks for the tests
'''

class CursorMock:
    '''
    Mock of DB cursor
    '''
    def __init__(self, throw: bool =False):
        self._throw = throw
        self._command = ""
        self._was_close = False

    def execute(self, command: str, _: str=''):
        '''
        Imitate execution
        '''
        if self._throw:
            self._throw = False
            raise Exception("test exception")
        self._command = command

    def close(self):
        '''
        Imitate closing
        '''
        self._was_close = True

    @property
    def command(self):
        '''
        Return command that was executed
        '''
        return self._command

    @property
    def was_closed(self):
        '''
        return close state
        '''
        return self._was_close


class ConnectionMock:
    '''
    Mock DB connection
    '''

    def __init__(self):
        self._was_commit = False
        self._was_close = False

    def commit(self):
        '''
        Imitate commit
        '''
        self._was_commit = True

    def close(self):
        '''
        Imitate close
        '''
        self._was_close = True

    @property
    def was_commit(self):
        '''
        Get commit status
        '''
        return self._was_commit

    @property
    def was_close(self):
        '''
        Get close status
        '''
        return self._was_close

def connect_to_db():
    '''
    Imitate connection to the DB
    '''
    return ConnectionMock(), CursorMock()

was_save: bool = False
def save_to_db(db: object, cursor: object, value: dict) -> None:
    '''
    Imitate DB saving
    '''
    global was_save
    was_save = True

class KafkaMock:
    '''
    Mock for the Kafka
    '''
    def __init__(self):
        pass


class MockKafkaMessage:
    '''
    Mock Kafka message
    '''
    def __init__(self, value: dict, timestamp: int):
        self.value = value
        self.timestamp = timestamp

def connect_to_kafka():
    '''
    Imitate connection to the Kafka 
    '''
    return [MockKafkaMessage('''{"site": "google.com",
                                 "status" : true,
                                 "elapsed": 1}''', 1),
            MockKafkaMessage('''{"site": "notagoogle.com",
                                 "status" : false,
                                 "elapsed": 1}''', 2)]

last_checked_site: str = ""
def check_site(url: str) -> dict:
    '''
    Imitate site checking
    '''
    global last_checked_site
    last_checked_site = url
    res: dict = {}
    res["status"] = True
    res["elapsed"] = 1
    return res

was_send_message: bool = False
def send_message(producer, topic, message):
    '''
    Imitate message sending
    '''
    global was_send_message
    was_send_message = True
