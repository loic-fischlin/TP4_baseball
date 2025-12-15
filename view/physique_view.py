import math
import time
from typing import TYPE_CHECKING

import pymunk
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor
from pymunk import Vec2d
from sympy.physics.units import velocity

if TYPE_CHECKING:
    from controlleur.controlleur import MainController


class PymunkSimulationWidget(QWidget):
    positionChanged = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.paused = False
        self.W, self.H = 896, 504
        self.setFixedSize(self.W, self.H)
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

        self.background = QPixmap("resources/background.png")
        self.ball_image = QPixmap("resources/balle.png")

        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.batte_spawn_position = None
        self.reset_batte = False
        self.init_simulation()

    def init_simulation(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, -981)

        ground_y = 50
        ground = pymunk.Segment(
            self.space.static_body,
            (-10000, ground_y),
            (10000, ground_y),
            2
        )
        ground.elasticity = 0.5
        ground.friction = 1
        ground.collision_type = 2
        self.space.add(ground)

        mass = 5
        self.radius = 20
        moment = pymunk.moment_for_circle(mass, 0, self.radius)

        self.ball = pymunk.Body(mass, moment)
        self.ball.position = (-1000, -1000)
        pitch_shape = pymunk.Circle(self.ball, self.radius)
        pitch_shape.elasticity = 1
        pitch_shape.friction = 1
        pitch_shape.collision_type = 1
        self.space.add(self.ball, pitch_shape)

        self.batte = pymunk.Body(mass, moment)
        self.batte.position = (-1000, -1000)
        drag_shape = pymunk.Circle(self.batte, self.radius)
        drag_shape.elasticity = 1
        drag_shape.friction = 1
        drag_shape.collision_type = 3
        self.space.add(self.batte, drag_shape)

        self.space.on_collision(1, 2, begin=self.on_ball_hit_ground)

    def update_simulation(self):
        dt = 1 / 60

        v = Vec2d(self.ball.velocity.x, self.ball.velocity.y)
        speed = v.length
        spin = self.ball.angular_velocity
        if speed > 0 and spin != 0:
            constante = 0.2

            direction = Vec2d(-v.y, v.x).normalized()
            force = constante * abs(spin) * speed * direction

            if spin < 0:
                force = -force

            self.ball.apply_force_at_local_point(force, (0, 0))

        if self.batte.position.x > 200 or self.batte.position.y > 200:
            self.batte.position = (-1000, -1000)
            self.batte.velocity = (0, 0)
        elif self.batte.velocity.x < 0:
            self.reset_batte = True

        ground_y = 50
        rebound_threshold = 5
        if self.ball.position.y - self.radius <= ground_y + rebound_threshold:
            vx, vy = self.ball.velocity
            self.ball.velocity = vx * 0.9, vy


        if self.ball.velocity.x < 10000000:
            self.positionChanged.emit(self.ball.position.x, self.ball.position.y - 50)

        self.space.step(dt)
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.dragging = True
        self.drag_start = event.position()
        self.drag_end = self.drag_start

        x_qt = event.position().x()
        y_qt = event.position().y()
        self.batte_spawn_position = Vec2d(x_qt, self.H - y_qt)

    def mouseMoveEvent(self, event):
        if not self.dragging:
            return
        self.drag_end = event.position()

    def mouseReleaseEvent(self, event):
        if not self.dragging or event.button() != Qt.MouseButton.LeftButton:
            return

        self.dragging = False
        self.drag_end = event.position()

        dx_qt = self.drag_end.x() - self.drag_start.x()
        dy_qt = self.drag_end.y() - self.drag_start.y()
        scale = 15.0
        impulse = Vec2d(dx_qt * scale, -dy_qt * scale)

        if self.batte_spawn_position is not None:
            self.batte.position = self.batte_spawn_position
        self.batte.velocity = (0, 0)
        self.batte.angular_velocity = 0
        self.batte.angle = 0

        self.batte.apply_impulse_at_local_point(impulse, (0, 0))

        self.drag_start = None
        self.drag_end = None

    def lancer(self, speed, spin):
        self.batte.position = (-1000, -1000)
        self.ball.position = (750, 150)
        self.ball.velocity = (0, 0)
        self.ball.angular_velocity = 0
        self.ball.angle = 0
        angle = -0.25

        velocity_x = -speed*10 * math.cos(angle)
        velocity_y = -speed*10 * math.sin(angle)
        self.ball.velocity = (velocity_x, velocity_y)
        self.ball.angular_velocity = spin*10

    def on_ball_hit_ground(self, arbiter, space, data):
        body = self.ball
        print("Touché au sol à:", body.position.x, body.position.y)

    def paintEvent(self, event):
        p = QPainter(self)

        p.drawPixmap(0, 0, self.W, self.H, self.background)

        for body in (self.ball, self.batte):

            if body is self.batte and self.reset_batte:
                self.reset_batte = False
                continue

            p.save()

            cx = body.position.x
            cy = self.H - body.position.y
            p.translate(cx, cy)

            angle_deg = -body.angle * 180.0 / math.pi
            p.rotate(angle_deg)

            if body is self.ball:
                if body is self.ball:
                    p.setClipRect(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
                    p.drawPixmap(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius, self.ball_image)

            else:
                p.setBrush(QColor(160, 82, 45))
                p.drawEllipse(-self.radius,-self.radius,2 * self.radius, 2 * self.radius
                )

            p.restore()

    def pause(self):
        if not self.paused:
            self.timer.stop()
            self.paused = True

    def resume(self):
        if self.paused:
            self.timer.start(16)
            self.paused = False

    def set_controller(self, controller):
        self.__controller = controller

