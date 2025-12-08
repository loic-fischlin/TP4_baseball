from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
if TYPE_CHECKING:
    from controlleur.controlleur import MainController


class GrapheCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        super().__init__(self.fig)
        if TYPE_CHECKING:
            self.__controller: MainController | None = None

    def set_controller(self,controller):
        self.__controller = controller