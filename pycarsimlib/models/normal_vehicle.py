""" normal vehicle model """
import os
from rich import print
from rich.panel import Panel
from rich.text import Text
from pycarsimlib.logger import initialize_logging
logger = initialize_logging(__name__)


class NormalVehicle:
    """ class to define normal vehicle model """
    def __init__(self) -> None:
        logger.info("Vehicle type : NormalVehicle")
        self._define_import_params()
        self._define_export_params()
        self.echo_command_for_carsim_gui()

    def _define_import_params(self):
        """ define control inputs """
        self.import_label_array = [
            "IMP_STEER_SW",
            "IMP_FBK_PDL",
            "IMP_THROTTLE_ENGINE"
        ]

    def _define_export_params(self):
        """ define variables to be observed """
        self.export_label_array = [
            "XCG_TM",
            "YCG_TM",
            "Yaw"
        ]

    def get_import_labels(self):
        """ getter of import value labels """
        return self.import_label_array.copy()

    def get_export_labels(self):
        """ getter of export value labels """
        return self.export_label_array.copy()

    def echo_command_for_carsim_gui(self):
        """ input those commands into 'Additional Data' in the carsim gui. """
        logger.warn("Do not forget to set following variables on carsim gui.")

        # generate command for carsim gui
        _cmd = os.linesep

        # add commands for import variables
        for imp in self.import_label_array:
            _cmd += "IMPORT " + imp + " Replace 0.0! 1" + os.linesep

        # add commands for export variables
        for exp in self.export_label_array:
            _cmd += "EXPORT " + exp + " Replace 0.0! 1" + os.linesep

        panel = Panel(Text(_cmd))
        print(panel)

