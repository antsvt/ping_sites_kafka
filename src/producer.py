'''
Ping site and put result to the Kafka
'''

import time
import json
import logging
import requests

from kafka import KafkaProducer

from config import Config
from handler import Handler


def extra_site_check(url: str) -> str:
    '''
    Dummy function in case if extra checks are needed
    '''
    return url


def check_site(url: str) -> dict:
    '''
    Check if site is available
    '''
    try:
        r = requests.get(url, timeout=1000)
        res = {}
        res["status"] = r.status_code == 200
        res["elapsed"] = r.elapsed.microseconds
        res["metadata"] = extra_site_check(url)

        logging.debug('Site %s returned code %d in %d ms',
                      url, r.status_code, r.elapsed.microseconds)

        return res

    except Exception as err:
        logging.warning('Request to the site %s returned error %s', url, err)
        return {}


def send_message(producer: KafkaProducer, topic: str, messege: str) -> None:
    '''
    Push results to the Kafka
    '''
    producer.send(topic, messege.encode('utf-8'))
    logging.debug('Message %s was sent to the topic %s',
                  messege, topic)


def serialize(data: dict) -> str:
    '''
    Serialize to the json format
    '''
    serialized_string = json.dumps(data)
    logging.info('Message is serealized to json:  %s', serialized_string)
    return serialized_string


def connect_to_kafka() -> KafkaProducer:
    '''
    Connect to Kafka
    '''
    logging.debug('Connecting to the kafka: %s:%s',
                  Config.kafka_host,
                  Config.kafka_port)

    return KafkaProducer(
        bootstrap_servers=[f'{Config.kafka_host}:{Config.kafka_port}'])


def run() -> None:
    '''
    Get list of sites, connect to the kafka and put results of the ping
    '''
    try:
        Handler.set_handler()
        producer = connect_to_kafka()

        while not Handler.should_exit:
            for url in Config.sites:
                result = check_site(url)
                result["site"] = url
                send_message(producer, Config.topic_name, serialize(result))

            if not Handler.should_exit:
                time.sleep(Config.interval_between_checks_in_sec)
    except Exception as err:
        logging.fatal('Got fatal error %s, stopping', err)


if __name__ == '__main__':
    logging.basicConfig(filename=Config.log_file_name,level=logging.WARNING)
    run()
