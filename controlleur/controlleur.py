
import view
from modele import modele
from modele.modele import Modele
from view.view import MainWindow


class MainController:
    __view: MainWindow
    __model:Modele

    def __init__(self, view, model, physique, canva):
        self.__view = view
        self.__model = model
        self.__physique = physique
        self.__canva = canva

    def change_speed(self,value):
        self.__model.speed = value

    def change_spin(self, value):
        self.__model.spin = value


