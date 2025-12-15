import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox

from controlleur.controlleur import MainController
from modele.modele import Modele
from view.graph_view import GraphCanvas
from view.physique_view import PymunkSimulationWidget
from view.view import MainWindow

if __name__ == '__main__':
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)
    sys.excepthook = qt_exception_hook

    app = QApplication(sys.argv)
    canvas = GraphCanvas()
    physique = PymunkSimulationWidget()
    window = MainWindow(physique)
    model = Modele()
    controlleur = MainController(window, model, physique, canvas)
    window.set_controller(controlleur)
    window.set_canvas(canvas)
    canvas.set_controller(controlleur)
    window.show()
    window.box_information()

    sys.exit(app.exec())
