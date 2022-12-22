""" main process of pycarsimlib"""
import pycarsimlib
from pycarsimlib.core import CarsimManager
from pycarsimlib.logger import initialize_logging
logger = initialize_logging(__name__)

def main() -> None:
    """ main process """
    logger.info(f"pycarsimlib version=={pycarsimlib.__version__}")

    cm = CarsimManager(
        simfile_path=r"C:\Users\Public\Documents\CarSim2022.1_Data\simfile.sim",
        vehicle_type="normal_vehicle",
    )

    # cm.run_all()

    cm.step()
