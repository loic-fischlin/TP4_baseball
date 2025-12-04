

class Modele():

    def __init__(self):
        self._spin = 0
        self._speed = 0

    @property
    def spin(self):
        return self._spin

    @spin.setter
    def spin(self, value):
        self._spin = value