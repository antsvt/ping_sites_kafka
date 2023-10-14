'''
Handle system signals like sigterm or sigint
'''

import signal
import logging

class Handler:
    '''
    Just set and handle system signals
    '''

    should_exit = False

    @staticmethod
    def handler(signum: int, _) -> None:
        '''
        React on the signal
        '''
        signame: str = signal.Signals(signum).name
        logging.info("Signal handler called with signal %s (%d). Shutting down!",
                    signame, signum)
        Handler.should_exit = True


    def set_handler(self) -> None:
        '''
        Set the signal handler for the TERM and INT signals
        '''
        signal.signal(signal.SIGTERM, Handler.handler)
        signal.signal(signal.SIGINT, Handler.handler)
        logging.info("Signals handler was registered int the system")
