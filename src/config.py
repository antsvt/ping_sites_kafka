'''
Dummy config. Use something smart in real project, like hydra
'''

from dataclasses import dataclass

@dataclass
class Config:
    '''
        Values from config should be loaded somehow. Password also should be somehow protected.
        This open text is just for POC.
    '''

    interval_between_checks_in_sec: int = 30
    sites: list = ["https://www.google.com",
                   "https://www.example.com",
                   "https://www.nonexistentwebsite.com"]

    table_name: str = "table_sites_status"
    db_host: str = "db"
    db_port: int = 5432
    db_database: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "postgres"

    topic_name: str = "topic_site_status"
    kafka_host: str = "kafka"
    kafka_port: int = 29092
    kafka_offset_reset: str = 'latest'
    kafka_group_id: str = 'site_status_group'

    log_file_name: str = "/dev/null"

    def __init__(self):
        pass
