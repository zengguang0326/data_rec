# -*- coding: utf8 -*-
import logging
from opcua import ua, Server
from kafka import KafkaConsumer
import json
from retrying import retry
# from server_all import main
from server_test import main

# logging.config.fileConfig('logging.conf', disable_existing_loggers=True)
# logger = logging.getLogger("simpleExample")
# logging.debug('debug message')
# logging.info("info message")
# logging.warn('warn message')
# logging.error("error message")
# logging.critical('critical message')
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def setupmain():
    main()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.ERROR)
    setupmain()
    input()