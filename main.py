import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from controlleur.controlleur import MainController
from modele.modele import Modele
from view.graph_view import GraphCanvas
from view.physique_view import PymunkSimulationWidget
from view.view import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = GraphCanvas()
    physique = PymunkSimulationWidget()
    window = MainWindow(physique)
    model = Modele()
    controlleur = MainController(window, model, physique, canvas)
    window.set_controller(controlleur)
    canvas.set_controller(controlleur)
    window.show()

    sys.exit(app.exec())
