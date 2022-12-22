""" normal vehicle model """
from pycarsimlib.logger import initialize_logging
logger = initialize_logging(__name__)

class NormalVehicle:
    """ class to define normal vehicle model """
    def __init__(self) -> None:
        logger.info("Vehicle type : NormalVehicle")
        pass
