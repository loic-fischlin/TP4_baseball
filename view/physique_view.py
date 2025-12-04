import math
import pymunk
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget
from pymunk import Vec2d


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
        handler = self.space.add_collision

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
        ground.collision_type = 2
        self.space.add(ground)

        # --- BOULE -----------------------------------------------
        mass = 5
        self.radius = 20
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (200, 300)
        shape = pymunk.Circle(self.body, self.radius)
        shape.elasticity = 0.8
        shape.friction = 0.9
        shape.collision_type = 1
        self.space.add(self.body, shape)



    def update_simulation(self):
        dt = 1 / 60

        v = Vec2d(self.body.velocity.x, self.body.velocity.y)
        speed = v.length

        # ---------- Résistance de l'air (optionnel, mais aide à stabiliser) ----------
        if speed > 0:
            k_drag = 0.01  # à ajuster
            drag_force = -k_drag * speed * v
            self.body.apply_force_at_local_point(drag_force, (0, 0))

        # ---------- Effet Magnus (rotation -> force latérale) ----------
        spin = self.body.angular_velocity  # >0 ou <0 selon le sens
        if speed > 0 and spin != 0:
            k_mag = 1  # coefficient de Magnus (augmente pour voir mieux l’effet)

            # vecteur perpendiculaire à la vitesse (90°)
            # si v = (vx, vy), un vecteur perpendiculaire = (-vy, vx)
            magnus_dir = Vec2d(-v.y, v.x).normalized()  # direction latérale
            magnus_force = k_mag * abs(spin) * speed * magnus_dir

            # changer le signe pour inverser le côté où ça courbe
            if spin < 0:
                magnus_force = -magnus_force

            self.body.apply_force_at_local_point(magnus_force, (0, 0))

        # ---------- Step physique ----------
        self.space.step(dt)
        self.update()

    # ------------------ SOURIS ------------------
    def mousePressEvent(self, event):
            # on "reset" un peu la balle pour éviter les vitesses accumulées
            self.body.position = (100, 200)
            self.body.velocity = (0, 0)
            self.body.angular_velocity = 0
            self.body.angle = 0

            # impulsion vers la droite et vers le haut -> parabole
            impulse = (2000, 2000)  # tu peux ajuster la puissance

            # on applique l'impulsion un peu au-dessus du centre
            # => ça crée un moment de rotation (spin)
            self.body.apply_impulse_at_local_point(impulse, (0, -self.radius))

    def on_ball_hit_ground(self, arbiter, space, data):
     body = self.body
     print("Touché au sol à:", body.position.x, body.position.y)
     return True

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
