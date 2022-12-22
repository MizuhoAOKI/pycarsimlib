""" core functions of pycarsimlib """

import os
import sys
import struct
import platform
import shutil
from pycarsimlib.api import vs_solver
from datetime import timedelta
from ctypes import cdll
from typing import Union, List, Dict, Any
from pycarsimlib.logger import initialize_logging
from pycarsimlib.models.normal_vehicle import NormalVehicle
from pycarsimlib.models.in_wheel_motored_vehicle import InWheelMotoredVehicle
logger = initialize_logging(__name__)


class CarsimManager:
    """ carsim manager """
    def __init__(
        self,
        carsim_db_dir: str,
        vehicle_type: str,
        **kwargs
    ) -> None:

        # set simfile path
        self.carsimdb_dir = carsim_db_dir
        self.simfile_path = os.path.join(self.carsimdb_dir, "simfile.sim")
        logger.info(f"simfile path : {self.simfile_path}")

        # select vehicle models
        if vehicle_type == "normal_vehicle":
            self.vehicle = NormalVehicle(**kwargs)
        elif vehicle_type == "in_wheel_motored_vehicle":
            self.vehicle = InWheelMotoredVehicle(**kwargs)
        else:
            logger.error(f"Invalid vehicle type '{vehicle_type}' is specified. ")
            raise AttributeError

        # initialize carsim solver
        self._init_carsim()

        # announce
        logger.info("Carsim solver has been initialized successfully.")

    def _init_carsim(self):
        """ init carsim """
        # get solver instance
        self.solver_api = vs_solver.vs_solver()
        self.path_to_vs_dll = self.solver_api.get_dll_path(self.simfile_path)

        if not self._is_system_available():
            logger.error("Carsim library is invalid.")
            raise RuntimeError

        if not self._is_solver_available():
            logger.error("Carsim solver is invalid.")
            raise RuntimeError

        # now, carsim solver is ready to use. loading params from simfile.
        self.configuration = self.solver_api.read_configuration(self.simfile_path)
        self.t_current = self.configuration.get('t_start')
        self.t_step = self.configuration.get('t_step')

        # prepare importation and exportation of variables
        self.num_of_import_values = self.configuration.get('n_import')
        self.num_of_export_values = self.configuration.get('n_export')
        self.import_label_array = self.vehicle.get_import_labels()
        self.export_label_array = self.vehicle.get_export_labels()
        self.export_array = self.solver_api.copy_export_vars(self.num_of_export_values)

    def _is_system_available(self):
        """ check if the carsim library is available in the system. """
        # dealing with different os
        current_os = platform.system()
        if self.path_to_vs_dll is not None \
                and os.path.exists(self.path_to_vs_dll):

            if current_os == "Linux":
                mc_type = platform.machine()
                if mc_type == 'x86_64':
                    dll_size = 64
                else:
                    dll_size = 32
            else:
                if "_64" in self.path_to_vs_dll:
                    dll_size = 64
                else:
                    dll_size = 32

        # check availability
        _system_word_size = (8 * struct.calcsize("P"))  # 32 or 64
        if _system_word_size != dll_size:
            print("Python size (32/64) must match size of .dlls being loaded.")
            print("Python size:", _system_word_size, "DLL size:", dll_size)
            return False
        else:
            return True

    def _is_solver_available(self):
        """ is solver available """
        try:
            self.vs_dll = cdll.LoadLibrary(self.path_to_vs_dll)
            if self.vs_dll is not None:
                if self.solver_api.get_api(self.vs_dll):
                    return True
        except Exception as err_msg:
            logger.error(err_msg)
            return False

    def reset(self):
        """ reset """
        # under developing
        raise NotImplementedError

    def step(self, action, delta_time):
        """ step run of carsim for delta_time with given action """
        _loop_num = delta_time // timedelta(seconds=self.t_step)

        for _ in range(_loop_num):

            # Run the integration loop
            self.t_current += self.t_step  # increment the time

            # reshape dict to list
            import_array = []
            for key in self.import_label_array:
                if key in action:
                    import_array.append(action[key])
                else:
                    logger.error("Invalid format of carsim action.")
                    raise AttributeError

            # call vs_api function
            status, self.export_array = self.solver_api.integrate_io(self.t_current, import_array, self.export_array)

        return dict(zip(self.export_label_array, self.export_array)), status, self.t_current

    def run_all(self):
        """ run all simulation steps at once """
        error_occurred = 1
        logger.info("##### Run all simulation steps #####")
        error_occurred = self.solver_api.run(
            self.simfile_path.replace('\\\\', '\\')
        )
        if error_occurred != 0:
            print("ERROR OCCURRED:  ")
            self.solver_api.print_error()
            sys.exit(error_occurred)
        logger.info("##### End of simulation #####")

    def close(self):
        """ close carsim solver normally"""
        self.solver_api.terminate_run(self.t_current)
        logger.info("Carsim solver terminated normally.")

    def save_results_into_carsimdb(self, results_source_dir="", results_target_dir=""):
        """ copy latest results dir into carsimdb location """

        # keep arguments
        _source_dir = results_source_dir
        _target_dir = results_target_dir

        # set paths
        if not _source_dir:
            _source_dir = os.path.join(os.getcwd(), "Results")
        if not _target_dir:
            _target_dir = os.path.join(self.carsimdb_dir, "Results")

        # copy results dir
        logger.info(f"Saving results into {_target_dir}")
        shutil.copytree(_source_dir, _target_dir, dirs_exist_ok=True)
        logger.info("Successfully saved results.")
