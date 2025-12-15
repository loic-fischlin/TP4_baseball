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

        self.__physique.positionChanged.connect(self.position_changed)
        self.__model.positionChanged.connect(self.__canva.update_position)


    def position_changed(self, x, y):
        self.__model.set_position(x, y)

    def change_speed(self,value):
        self.__model.speed = value

    def change_spin(self, value):
        self.__model.spin = value

    def throw_ball(self):
        print("throw ball")
        self.__canva.start_new_trajectory()
        self.__physique.lancer(self.__model.speed, self.__model.spin)

    def pause(self):
        self.__physique.pause()

    def resume(self):
        self.__physique.resume()

    def shrink_graph(self):
        self.__canva.set_lim(-200, 850, 0, 300)

    def expend_graph(self):
        self.__canva.set_lim(1000, 10000, 0, 4000)



