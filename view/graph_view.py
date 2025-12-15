from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.cm as cm

if TYPE_CHECKING:
    from controlleur.controlleur import MainController

class GraphCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.__fig, self.__ax = plt.subplots()
        super().__init__(self.__fig)

        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.current_x = []
        self.current_y = []

        self.__ax.set_xlim(-100, 10000)
        self.__ax.set_ylim(0, 4000)

        self.current_line, = self.__ax.plot([], [], 'r-')

    def start_new_trajectory(self):
        self.current_x = []
        self.current_y = []

        self.current_line.set_data([], [])
        self.draw_idle()

    def update_position(self, x, y):
        # print(x, y)
        self.current_x.append(x)
        self.current_y.append(y)

        self.current_line.set_data(self.current_x, self.current_y)

        self.draw_idle()

    def set_controller(self,controller):
        self.__controller = controller


    def set_lim(self, min_x, max_x, min_y, max_y):
        self.__ax.set_xlim(min_x, max_x)
        self.__ax.set_ylim(min_y, max_y)






