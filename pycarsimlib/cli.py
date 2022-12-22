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
    logger.info("Starting sample run. ")

    # instantiate carsim manager
    cm = CarsimManager(
        simfile_path=r"C:\Users\Public\Documents\CarSim2022.1_Data\simfile.sim",
        vehicle_type="normal_vehicle",
    )

    # set simulation params
    onestep_delta_time = timedelta(seconds=0.1)
    total_sim_time = timedelta(minutes=0.5)
    total_sim_step = total_sim_time // onestep_delta_time

    # run simulation steps
    try:
        for _ in track(range(total_sim_step), description="Running simulation..."):

            # prepare operational signals
            control_inputs = {
                "IMP_STEER_SW": 10.0,
                "IMP_FBK_PDL": 1.0,
                "IMP_THROTTLE_ENGINE": 5.0
            }

            # update vehicle states
            observed, terminated, updated_time_sec = cm.step(action=control_inputs, delta_time=onestep_delta_time)

            # output log
            # logger.info(f"T = {updated_time_sec:.2f} [s]")
            # logger.info(observed)

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

    # save results to check results with vs_visualizer
    cm.save_results_into_carsimdb(
        results_source_dir=r"C:\Users\mizuho\carsim\Results",
        results_target_dir=r"C:\Users\Public\Documents\CarSim2022.1_Data\Results"
    )
