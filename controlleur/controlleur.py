from idlelib.debugobj_r import remote_object_tree_item

from IPython.terminal.shortcuts.auto_suggest import resume_hinting

import view
from modele import modele
from modele.modele import Modele
from view.graph_view import GraphCanvas
from view.physique_view import PymunkSimulationWidget
from view.view import MainWindow


class MainController:
    __view: MainWindow
    __model:Modele
    __physique: PymunkSimulationWidget
    __canva: GraphCanvas

    def __init__(self, view, model, physique, canva):
        self.__view = view
        self.__model = model
        self.__physique = physique
        self.__canva = canva

    def position_changed(self, x, y):
        return

    def change_speed(self,value):
        self.__model.speed = value

    def change_spin(self, value):
        self.__model.spin = value

    def throw(self):
        self.__physique.lancer(self.__model.speed, self.__model.spin)

    def pause(self):
        return

    def resume(self):
        return


