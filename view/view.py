from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QDoubleSpinBox, QPushButton, QVBoxLayout
from PyQt6.uic import loadUi

from view.graph_view import GraphCanvas
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

        self.spinBox_spin.setRange(-150,150)
        self.spinBox_speed.setRange(0,100)

        #barre de contrôle
        self.spinBox_speed.valueChanged.connect(self.speed_changed)
        self.spinBox_spin.valueChanged.connect(self.spin_changed)
        self.throw_button.clicked.connect(self.throw)
        self.pause_button.clicked.connect(self.pause)
        self.resume_button.clicked.connect(self.resume)

        canvas = GraphCanvas()
        self.grapheLayout.addWidget(canvas)




    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_T:
            self.throw()

    def speed_changed(self, value):
        self.__controller.change_speed(value)

    def spin_changed(self, value):
        self.__controller.change_spin(value)

    def throw(self):
        self.__controller.throw_ball()

    def pause(self):
        self.__controller.pause()

    def resume(self):
        self.__controller.resume()

    def add_canvas(self, canvas):
        self.grapheLayout.addWidget(canvas)

    def set_controller(self,controller):
        self.__controller = controller




