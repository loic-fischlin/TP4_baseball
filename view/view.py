from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QDoubleSpinBox, QPushButton, QVBoxLayout
from PyQt6.uic import loadUi

from view.physique_view import PymunkSimulationWidget

if TYPE_CHECKING:
    from controlleur.controlleur import MainController


class MainWindow(QMainWindow):
    grapheLayout:QVBoxLayout

    layout_jeu : QHBoxLayout
    spinBox_speed : QDoubleSpinBox
    spinBox_spin : QDoubleSpinBox
    throw_button : QPushButton
    pause_button : QPushButton
    resume_button : QPushButton

    def __init__(self):
        super().__init__()
        loadUi("view/ui/baseball.ui", self)

        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.jeu = PymunkSimulationWidget()
        self.layout_jeu.addWidget(self.jeu)

        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.spinBox_speed.valueChanged.connect(self.speed_changed)


    def speed_changed(self, value):
        self.__controller.change_speed(value)

    def add_canvas(self, canvas):
        self.grapheLayout.addWidget(canvas)

    # def add_physique(self, physique):
    #     self.layout_jeu.addWidget(physique)

    def set_controller(self,controller):
        self.__controller = controller




