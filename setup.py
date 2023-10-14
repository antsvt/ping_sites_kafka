import os
from setuptools import setup

setup(
    name = "ping-sites-kafka",
    version = "1.1",
    author = "Anatolii Sviridenkov",
    author_email = "anatoliy.sviridenkov@gmail.com",
    description = "Test task",
    license = "BSD",
    packages=['src'],
    install_requires=[
       "requests",
       "psycopg2-binary",
       "kafka-python",
   ],
)
