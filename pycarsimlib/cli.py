""" main process of pycarsimlib"""
import pycarsimlib
from pycarsimlib.logger import initialize_logging
logger = initialize_logging(__name__)


def main() -> None:
    """ echo version """
    logger.info(f"pycarsimlib version=={pycarsimlib.__version__}")
