# Table of content

1. Requerements
1. Docker
1. Build
1. Notes

## Requirements

For use/build project you need python3 with installed unittest package. Also if you going to run/test scripts on local machine, please notice requirements.txt

## Docker

For start test environment on your local PC, please check if you have docker and docker copose installed.

For start environment: docker-compose up
For stop environment: docker-compose down

## Build

Starting build.sh should be enough. As result of the build will be generated python package.

## Notes

Project consists from 3 file:
1. producer.py - run this file for starting site availability status collecting. It saves resuts to the Kafka.
2. consumer.py - run this file for save results from Kafka to PostgreSQL
3. confit.py - please check options, may be you need to change setting for running this in your environment.