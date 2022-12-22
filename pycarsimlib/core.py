""" class to plot manipulator """

import os
import sys
import struct
import platform
import time
from pycarsimlib.api import vs_solver
from datetime import timedelta
from ctypes import cdll
from time import sleep
from typing import Union, List, Dict, Any
from pycarsimlib.logger import initialize_logging
from pycarsimlib.models.normal_vehicle import NormalVehicle
from pycarsimlib.models.in_wheel_motored_vehicle import InWheelMotoredVehicle
logger = initialize_logging(__name__)


class CarsimManager:
    """ carsim manager """
    def __init__(
        self,
        simfile_path: str,
        vehicle_type: str,
        **kwargs
    ) -> None:

        # set simfile path
        self.simfile_path = simfile_path
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

    def _init_carsim(self):
        """ init carsim """
        self.solver_api = vs_solver.vs_solver()
        self.system_word_size = (8 * struct.calcsize("P"))  # 32 or 64
        self.path_to_vs_dll = self.solver_api.get_dll_path(self.simfile_path)

        if not self._is_system_available():
            logger.error("Carsim library is invalid.")
            raise RuntimeError

        if not self._is_solver_available():
            logger.error("Carsim solver is invalid.")
            raise RuntimeError

        self.configuration = self.solver_api.read_configuration(self.simfile_path)
        self.t_current = self.configuration.get('t_start')
        self.t_step = self.configuration.get('t_step')

        # ここらの変数受け渡しをかしこく指定する.
        # Create import and export arrays based on sizes from VS solver
        self.import_array = [0.0, 0.0]
        self.export_array = self.solver_api.copy_export_vars(self.configuration.get('n_export'))
        # 警告
        # if (len(self.export_array) < 3):
        #     print("At least three export parameters needed.")

    def _is_system_available(self):
        """ check if the carsim library is available in the system. """
        # dealing with different os
        current_os = platform.system()
        if self.path_to_vs_dll is not None \
                and os.path.exists(self.path_to_vs_dll):

            if current_os == "Linux":
                mc_type = platform.machine()
                if mc_type == 'x86_64':
                    self.dll_size = 64
                else:
                    self.dll_size = 32
            else:
                if "_64" in self.path_to_vs_dll:
                    self.dll_size = 64
                else:
                    self.dll_size = 32

        # check availability
        if self.system_word_size != self.dll_size:
            print("Python size (32/64) must match size of .dlls being loaded.")
            print("Python size:", self.system_word_size, "DLL size:", self.dll_size)
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
        self.close()
        time.sleep(5.0)
        self._init_carsim()

    def step(self, action, delta_time):
        """ step """
        # デバッグ中
        # import, export周りをmodels/からインポートしたクラス使って上手いことやる.

        _loop_num = delta_time // timedelta(seconds=self.t_step)

        for _ in range(_loop_num):

            # Run the integration loop
            self.t_current += self.t_step  # increment the time

            # Steering Controller variables, based on previous exports
            x_center_of_gravity = self.export_array[0]
            y_center_of_gravity = self.export_array[1]
            _degrees_to_radians_scale_factor = 180.0 / 3.1415
            yaw = self.export_array[2] / _degrees_to_radians_scale_factor  # convert export deg to rad

            # copy values for 3 variables that the VS solver will import
            import_array = [-1.0, 10.0, 10.0] # actionを入れる.

            # Call the VS API integration function
            status, self.export_array = self.solver_api.integrate_io(self.t_current, import_array, self.export_array)

            # dummy info
            info = ""

        return [x_center_of_gravity, y_center_of_gravity, yaw], status, info

    def run_all(self):
        """ run all """
        error_occurred = 1
        logger.info("##### Run all simulation steps #####")
        error_occurred = self.solver_api.run(
            self.simfile_path.replace('\\\\', '\\')
        )
        if error_occurred != 0:
            print("ERROR OCCURRED:  ")
            self.solver_api.print_error()
            sys.exit(error_occurred)
        logger.info("##### Ending run #####")

    def close(self):
        """ close """
        # Terminate solver
        self.solver_api.terminate_run(self.t_current)
        logger.info("Carsim solver terminated normally.")
