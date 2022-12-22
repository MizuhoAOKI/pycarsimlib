""" class to define 'scara' manipulator model """
from typing import Union, List, Dict, Any
from maniviz.utils.logger import initialize_logging
import rich
import numpy as np
logger = initialize_logging(__name__)

class ScaraManipulator:
    """ class to define manipulator model """
    def __init__(
        self,
        num_of_links: int = 2,
        len_of_links: List[float] = [1.0, 1.0],
        base_pos: List[float] = [1.0, 1.0],
        initial_state_type: str = "joint_angles", # "joint_angles, joint_positions"
        initial_joint_angles: List[float] = [0.3, 0.6],
        initial_joint_positions_xy: List[Union[float, float]] = [[0.5, 0.5], [1.5, 1.5]],
        ) -> None:

        # save arguments
        self.num_of_links = num_of_links # == (num of joints)
        if self.num_of_links < 1:
            logger.error("Invalid value of num_of_links is specified.")
            raise AttributeError
        self.len_of_links = len_of_links
        self.base_pos = base_pos

        # declare state variables
        self.joint_positions_xy = initial_joint_positions_xy
        self.joint_angles = initial_joint_angles

        # calculate manipulator attitude
        if initial_state_type == "joint_angles":
            self.update_attitude_with_joint_angles()
        elif initial_state_type == "joint_positions_xy":
            self.update_attitude_with_joint_positions()
        else:
            logger.error(f"Invalid initial_state_type '{initial_state_type}' is specified. ")
            raise AttributeError

        # announcement
        logger.debug("Finish building a SCARA manipulator")

    def echo_info(self):
        """ display manipulator's info """
        # Title panel
        rich.print(
            rich.panel.Panel(rich.text.Text("Info of the SCARA Manipulator", justify="left"), expand=False)
        )

        # Print table of joints
        _console = rich.console.Console()
        _table = rich.table.Table(show_header=True, header_style="bold")
        _table.add_column("Joint Number", justify="center")
        _table.add_column("Link Length (m)", justify="center")
        _table.add_column("Angle (rad) ", justify="center")
        _table.add_column("Position [X(m),Y(m)]", justify="center")
        for i in range(self.num_of_links):
            _format_pos_str = []
            for pos in self.joint_positions_xy[i]:
                _format_pos_str.append(float(f"{pos:.3f}"))
            _table.add_row(str(i), f"{self.len_of_links[i]:.1f}", f"{self.joint_angles[i]:.3f}", f"{_format_pos_str}")
        _console.print(_table)

    def get_params(self) -> Dict[str, Any]:
        """ return parameters """
        _params = {
            "num_of_links":self.num_of_links,
            "base_pos" : self.base_pos,
            "len_of_links" : self.len_of_links
            }
        return _params

    def get_joint_angles(self) -> List[float]:
        """ return list of joint angles """
        return self.joint_angles

    def get_joint_positions(self) -> List[Union[float, float]]:
        """ return list of joint positions """
        return self.joint_positions_xy

    def set_joint_angles(self, joint_angles:List[float]) -> None:
        """ set joint angles """
        self.joint_angles = joint_angles
        self.update_attitude_with_joint_angles()

    def set_joint_positions(self, joint_positions_xy:List[Union[float, float]]):
        """ set joint positions """
        self.joint_positions_xy = joint_positions_xy
        self.update_attitude_with_joint_positions()

    def update_attitude_with_joint_angles(self) -> None:
        """ use forward kinematics and update joint positions with latest joint angles """
        # clear joint positions
        self.joint_positions_xy = [self.base_pos]

        _len = self.len_of_links
        _angle_cumsum = np.cumsum(self.joint_angles)

        for i in range(self.num_of_links):
            _pos = self.joint_positions_xy[-1]
            _new_pos = [0.0, 0.0]
            _new_pos[0] = _pos[0] + _len[i] * np.cos(_angle_cumsum[i]) # x pos
            _new_pos[1] = _pos[1] + _len[i] * np.sin(_angle_cumsum[i]) # y pos
            self.joint_positions_xy.append(_new_pos)

    def update_attitude_with_joint_positions(self) -> None:
        """ use forward kinematics and update joint angles with latest joint positions """
        raise NotImplementedError
