import sys

from PyQt6.QtWidgets import QApplication

from view.view import PymunkSimulationWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PymunkSimulationWidget()
    window.show()
    sys.exit(app.exec())
