'''
Get results from Kafka and put to the DB.
'''

import json
import logging

import psycopg2 as dbapi2
from psycopg2 import Error
from kafka import KafkaConsumer

from utils.config import Config
from utils.handler import Handler

def create_status_table_if_needed(db: object, cursor: object) -> None:
    '''
    Check db andprepare table for status of checked sites
    '''
    try:
        cursor.execute(f'SELECT 1 FROM {Config.table_name} LIMIT 1;')
        logging.debug('Table %s exists', Config.table_name)

    except (Exception, Error) as _:
        db.commit()
        logging.debug('Table %s already exists', Config.table_name)
        create_table_query = f'''CREATE TABLE {Config.table_name}
                                    (SITE        TEXT NOT NULL,
                                     STATUS_WHEN TIMESTAMP,
                                     STATUS      TEXT,
                                     ELAPSED     INT,
                                     PRIMARY KEY(SITE, STATUS_WHEN)); '''
        cursor.execute(create_table_query)
    finally:
        db.commit()


def connect_to_db() -> tuple(object, object):
    '''
    Connect to the DB with data from config
    '''
    try:
        db = dbapi2.connect(host=Config.db_host,
                            port=Config.db_port,
                            database=Config.db_database,
                            user=Config.db_user,
                            password=Config.db_password)
        cursor = db.cursor()

        logging.debug('Connected to %s:%d', Config.db_host, Config.db_port)

        create_status_table_if_needed(db, cursor)
        return db, cursor
    except (Exception, Error) as error:
        logging.fatal('Fatal error while connecting to PostgreSQL %s', error)


def save_status_to_db(db: object, cursor: object, value: dict) -> None:
    '''
    Push site stuatus to db
    '''
    try:
        cursor.execute(f'''INSERT INTO {Config.table_name} 
                        (SITE, STATUS_WHEN, STATUS, ELAPSED)
                        VALUES(%s, to_timestamp(%s), %s, %s)''',
                        (value["site"], value["when"],
                        value["status"], value["elapsed"]))

        logging.info('Message %s, %s, %s, %s is saved to %s',
                     value["site"],
                     value["when"],
                     value["status"],
                     value["elapsed"],
                     Config.table_name)

    except (Exception, Error) as error:
        logging.error('Can not save data to db, error: %s', error)
    finally:
        db.commit()


def connect_to_kafka() -> object:
    '''
    Connect to the Kafka with data from config
    '''
    return KafkaConsumer(
        Config.topic_name,
        bootstrap_servers=[f'{Config.kafka_host}:{Config.kafka_port}'],
        auto_offset_reset=Config.kafka_offset_reset,
        enable_auto_commit=True,
        group_id=Config.kafka_group_id,
        value_deserializer=lambda x: x.decode('utf-8'))


def deserialize(message: str) -> dict:
    '''
    Exctract data from json string
    '''
    value = json.loads(message.value)
    value["when"] = message.timestamp

    logging.info('Message is deserealized from json: %s', message.value)

    return value


def run() -> None:
    '''
    Put events from Kafka to DB
    '''
    Handler.set_handler()
    db, cursor = connect_to_db()
    consumer = connect_to_kafka()

    for message in consumer:
        value = deserialize(message)
        save_status_to_db(db, cursor, value)
        if Handler.should_exit:
            break

    cursor.close()
    db.close()


if __name__ == '__main__':
    logging.basicConfig(filename=Config.log_file_name,level=logging.WARNING)
    run()
