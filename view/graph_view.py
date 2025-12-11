from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
if TYPE_CHECKING:
    from controlleur.controlleur import MainController

class GraphCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.__fig, self.__ax = plt.subplots()
        super().__init__(self.__fig)

        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.plot()

    def plot(self):
        x = np.linspace(0,10,100)
        y = np.sin(x)
        self.__ax.plot(x,y)

    def set_controller(self,controller):
        self.__controller = controller