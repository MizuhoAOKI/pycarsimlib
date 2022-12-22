""" class to plot manipulator """
from typing import Union, List, Dict, Any
from pycarsimlib.logger import initialize_logging
from matplotlib import pyplot as plt
from matplotlib import patches
from maniviz.models.scara_model import ScaraManipulator
import os
import numpy as np
logger = initialize_logging(__name__)

class ManipulatorVisualizer:
    """ manipulator visualizer """
    def __init__(
        self,
        manipulator_type: str="scara",
        fig_xlim : Union[float, float] = [],
        fig_ylim : Union[float, float] = [],
        fig_zlim : Union[float, float] = [],
        **kwargs
        ) -> None:

        # save arguments
        self.manipulator_type = manipulator_type
        self.fig_xlim = fig_xlim
        self.fig_ylim = fig_ylim
        self.fig_zlim = fig_zlim

        # call constructor of the specified type of a manipulator
        if self.manipulator_type == "scara": # corresponding to 2d visualization
            self.mani_obj = ScaraManipulator(**kwargs)
            # initialize a figure
            self._init_scara_plot()
        elif self.manipulator_type == "vertical_multi_jointed": # corresponding to 3d visualization
            raise NotImplementedError
        else:
            logger.error(f"Invalid manipulator type '{manipulator_type}' is specified. ")
            raise AttributeError

    def _init_scara_plot(self):
        # make a figure and an axis object
        self.fig = plt.figure(figsize=(15, 15))
        self.ax = self.fig.add_subplot(111)

        # create circle objects to draw joints
        self.joint_circle_patches = []

        # get manipulator params
        _p = self.get_params()
        _joint_positions_xy = self.get_joint_potisions()

        # parameters
        _base_facecolor = "black"
        _base_edgecolor = "black"
        _normal_facecolor = "white"
        _normal_edgecolor = "black"

        for i in range(_p["num_of_links"]-1):

            # normal joint settings
            _facecolor = _normal_facecolor
            _edgecolor = _normal_edgecolor

            # base joint settings
            if i==0:
                _facecolor = _base_facecolor
                _edgecolor = _base_edgecolor

            # add a joint circle
            _joint_circle_patch = patches.Circle(
                xy=_joint_positions_xy[i],
                radius=_p["len_of_links"][0]/5,
                facecolor=_facecolor,
                angle=0,
                edgecolor=_edgecolor,
                linewidth=3,
                linestyle="solid",
                zorder=10,
            )
            self.ax.add_patch(_joint_circle_patch)
            self.joint_circle_patches.append(_joint_circle_patch)

        # create line objects to draw links
        _links_pos_x = []
        _links_pos_y = []
        for i in range(_p["num_of_links"]):
            _links_pos_x.append(_joint_positions_xy[i][0])
            _links_pos_y.append(_joint_positions_xy[i][1])
        self.link_line, = self.ax.plot(_links_pos_x, _links_pos_y, linewidth=5, color="#005AFF")

        # set layouts
        self.ax.set_aspect("equal")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        # set axis range
        _max_link_total_len = sum(_p["len_of_links"])

        # set x range
        if self.fig_xlim:
            # manual setting
            self.set_xlim(self.fig_xlim)
        else:
            # auto setting
            self.set_xlim(
                [
                _p["base_pos"][0] - _max_link_total_len,
                _p["base_pos"][0] + _max_link_total_len
                ]
            )

        # set y range
        if self.fig_ylim:
            # manual setting
            self.set_ylim(self.fig_xlim)
        else:
            # auto setting
            self.set_ylim(
                [
                _p["base_pos"][1] - _max_link_total_len,
                _p["base_pos"][1] + _max_link_total_len
                ]
            )

    def echo_info(self) -> None:
        """ notice this manipulator's description """
        self.mani_obj.echo_info()

    def get_params(self) -> Dict[str, Any]:
        """ return parameters """
        return self.mani_obj.get_params()

    def get_joint_angles(self) -> List[float]:
        """ return list of joint angles """
        return self.mani_obj.get_joint_angles()

    def get_joint_potisions(self) -> List[Union[float, float]]:
        """ return list of joint positions """
        return self.mani_obj.get_joint_positions()

    def set_joint_angles(self, arg) -> None:
        """ set joint angles """
        self.mani_obj.set_joint_angles(arg)

    def set_joint_positions(self, *args) -> None:
        """ set joint angle positions """
        self.mani_obj.set_joint_angles(args)

    def update_fig_elements(self) -> None:
        """ update location of joint circles and links """

        # get latest manipulator params and states
        _p = self.get_params()
        _latest_joint_positions_xy = self.get_joint_potisions()

        # update joints
        for i in range(self.mani_obj.num_of_links-1):
            self.joint_circle_patches[i].center = _latest_joint_positions_xy[i]

        # update links
        _links_pos_x = []
        _links_pos_y = []
        for i in range(self.mani_obj.num_of_links):
            _links_pos_x.append(_latest_joint_positions_xy[i][0])
            _links_pos_y.append(_latest_joint_positions_xy[i][1])
        self.link_line.set_data(_links_pos_x, _links_pos_y)

    def set_xlim(self, arg) -> None:
        """ set xlim of the figure """
        self.ax.set_xlim(arg)

    def set_ylim(self, arg) -> None:
        """ set ylim of the figure """
        self.ax.set_ylim(arg)

    def showfig(self) -> None:
        """ show figure """
        plt.show()

    def savefig(self, filename="result.png", dirname="./outputs") -> None:
        """ save figure """
        self.fig.savefig(os.path.join(dirname, filename))

    def updatefig(self, duration=10000000) -> None:
        """ update figure for 'duration' [sec] """
        self.update_fig_elements()
        plt.pause(duration)

if __name__=="__main__":

    # plot example
    m = ManipulatorVisualizer(
        manipulator_type="scara",
        fig_xlim=[],
        fig_ylim=[],
        num_of_links= 5,
        len_of_links=[1.0, 2.0, 3.0, 4.0, 5.0],
        base_pos = [-1.0, 3.0],
        initial_state_type = "joint_angles", # "joint_angles" or "joint_positions"
        initial_joint_angles = [0.3, 0.6, 0.9, 0.6, 0.3],
    )
    m.echo_info()
    m.savefig()

    # just show a figure
    # m.showfig()

    # animate figures
    for i in range(100):
        _buf = m.get_joint_angles()
        _buf[0] = np.sin(i/10)
        m.set_joint_angles(_buf)
        m.updatefig(duration=0.1)
