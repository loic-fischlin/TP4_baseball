import math
import pymunk
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget


class PymunkSimulationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.W, self.H = 600, 400
        self.setFixedSize(self.W, self.H)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

        self.init_simulation()

    def init_simulation(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, -900)

        # --- SOL -------------------------------------------------
        ground_y = 50
        ground = pymunk.Segment(
            self.space.static_body,
            (0, ground_y),
            (self.W, ground_y),
            2
        )
        ground.elasticity = 0.8
        ground.friction = 1.0
        self.space.add(ground)

        # --- BOULE -----------------------------------------------
        mass = 5
        self.radius = 20
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (200, 300)
        shape = pymunk.Circle(self.body, self.radius)
        shape.elasticity = 0.8
        shape.friction = 0.9  # friction pour faire tourner quand ça roule
        self.space.add(self.body, shape)

    def update_simulation(self):
        dt = 1 / 60
        self.space.step(dt)
        self.update()

    # ------------------ SOURIS ------------------
    def mousePressEvent(self, event):
            # on "reset" un peu la balle pour éviter les vitesses accumulées
            self.body.position = (100, 100)
            self.body.velocity = (0, 0)
            self.body.angular_velocity = 0

            # impulsion vers la droite et vers le haut -> parabole
            impulse = (800, 400)  # tu peux ajuster la puissance

            # on applique l'impulsion un peu au-dessus du centre
            # => ça crée un moment de rotation (spin)
            self.body.apply_impulse_at_local_point(impulse, (0, self.radius))

    # ------------------ DESSIN ------------------
    def paintEvent(self, event):
        p = QPainter(self)

        # --- Sol ---
        p.setBrush(Qt.GlobalColor.gray)
        p.drawRect(
            0,
            self.H - 50,  # Qt = Y vers le bas
            self.W,
            50
        )

        # --- Balle avec rotation ---
        p.save()

        # centre de la balle en coordonnées Qt
        cx = self.body.position.x
        cy = self.H - self.body.position.y  # inversion Y pour Qt

        # on place le repère au centre de la balle
        p.translate(cx, cy)

        # Pymunk: angle en radians, on convertit en degrés
        angle_deg = -self.body.angle * 180.0 / math.pi
        p.rotate(angle_deg)

        # on dessine le disque centré en (0,0)
        p.setBrush(Qt.GlobalColor.red)
        p.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

        # petit point pour voir la rotation
        p.setBrush(Qt.GlobalColor.white)
        # un point sur le bord droit de la balle
        p.drawEllipse(self.radius - 5, -5, 10, 10)

        p.restore()
