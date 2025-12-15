from PyQt6.QtCore import pyqtSignal, QObject


class Modele(QObject):

    positionChanged = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self._spin = 0
        self._speed = 0
        self._x = 0
        self._y = 0

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self.positionChanged.emit(x, y)

    @property
    def spin(self):
        return self._spin

    @spin.setter
    def spin(self, value):
        self._spin = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value