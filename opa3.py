import logging

logging.basicConfig(filename='rdt.log', filemode='w', level = 'DEBUG', format='%(name)s - %(levelname)s - %(message)s')
logging.debug("This is a debug message")