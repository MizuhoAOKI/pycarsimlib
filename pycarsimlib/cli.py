""" main process of pycarsimlib"""
import pycarsimlib
from datetime import timedelta
from pycarsimlib.core import CarsimManager
from pycarsimlib.logger import initialize_logging
from rich.progress import track
logger = initialize_logging(__name__)

def main() -> None:
    """ sample run """
    logger.info(f"pycarsimlib version=={pycarsimlib.__version__}")

    # instantiate carsim manager
    cm = CarsimManager(
        simfile_path=r"C:\Users\Public\Documents\CarSim2022.1_Data\simfile.sim",
        vehicle_type="normal_vehicle",
    )

    # set simulation params
    onestep_delta_time = timedelta(seconds=0.01)
    total_sim_time = timedelta(minutes=0.5)
    total_sim_step = total_sim_time // onestep_delta_time

    # run simulation steps
    try:
        for _ in track(range(total_sim_step), description="Running simulation..."):
            observe, terminated, info = cm.step(action=[], delta_time=onestep_delta_time)

            # check termination flag
            if terminated:
                logger.info("Termination flag is True. End of simulation.")
                break
    except KeyboardInterrupt:
        logger.warn("Process interrupted with Ctrl + C. ")
    except Exception as err_msg:
        logger.error(err_msg)

    # close carsim
    cm.close()

