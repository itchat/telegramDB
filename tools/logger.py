import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='tgnotes.log',
                    filemode='a',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
