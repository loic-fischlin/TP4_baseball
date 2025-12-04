import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDoubleSpinBox, QPushButton
from PyQt6.uic import loadUi
from PyQt6.uic.uiparser import QtWidgets

from view.physique_view import PymunkSimulationWidget


class MainWindow(QMainWindow):
    layout_jeu = QHBoxLayout
    spinBox_speed = QDoubleSpinBox
    spinBox_spin = QDoubleSpinBox
    throw_button = QPushButton
    pause_button = QPushButton
    resume_button = QPushButton

    def __init__(self):
        super().__init__()
        loadUi("view/ui/baseball.ui", self)

        self.jeu = PymunkSimulationWidget()
        self.layout_jeu.addWidget(self.jeu)





