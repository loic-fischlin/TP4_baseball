import math
import pymunk
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget
from pymunk import Vec2d


class PymunkSimulationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.W, self.H = 1280, 720
        self.setFixedSize(self.W, self.H)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

        self.background = QPixmap("resources/background.png")

        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.batte_spawn_position = None

        self.init_simulation()

    def init_simulation(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, -900)

        ground_y = 50
        ground = pymunk.Segment(
            self.space.static_body,
            (0, ground_y),
            (self.W, ground_y),
            2
        )
        ground.elasticity = 0.2
        ground.friction = 1.0
        ground.collision_type = 2
        self.space.add(ground)

        mass = 5
        self.radius = 20
        moment = pymunk.moment_for_circle(mass, 0, self.radius)

        self.ball = pymunk.Body(mass, moment)
        self.ball.position = (1050, 200)
        self.ball_shape = pymunk.Circle(self.ball, self.radius)
        self.ball_shape.elasticity = 1
        self.ball_shape.friction = 1
        self.ball_shape.collision_type = 1
        self.ball.body_type = pymunk.Body.KINEMATIC
        self.space.add(self.ball, self.ball_shape)

        self.batte = pymunk.Body(mass, moment)
        self.batte.position = (200, 900)
        self.batte_shape = pymunk.Circle(self.batte, self.radius)
        self.batte_shape.elasticity = 1
        self.batte_shape.friction = 1
        self.batte_shape.collision_type = 1
        self.batte.body_type = pymunk.Body.KINEMATIC
        self.space.add(self.batte, self.batte_shape)

        self.space.on_collision(1,2, begin = self.on_ball_hit_ground)
        self.space.on_collision(1,1, begin= self.on_ball_hit_batte)

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
        self.batte.body_type = pymunk.Body.DYNAMIC
        self.batte.activate()

        self.batte.apply_impulse_at_local_point(impulse, (0, 0))

        self.drag_start = None
        self.drag_end = None
        self.drag_spawn_world = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_P:
            self.lancer()

    def lancer(self):
            self.ball.position = (1050, 200)
            self.ball.velocity = (0, 0)
            self.ball.angular_velocity = 0
            self.ball.angle = 0
            self.ball.body_type = pymunk.Body.DYNAMIC
            self.ball.activate()

            impulse = (-4500, 2000)

            self.ball.apply_impulse_at_local_point(impulse, (0, 0))
            self.ball.angular_velocity = 100

    def on_ball_hit_ground(self, arbiter, space, data):
     body = self.ball
     print("Touché au sol à:", body.position.x, body.position.y)

    def on_ball_hit_batte(self, arbiter, space, data):
        self.batte.position = (200, 200)
        self.batte.body_type = pymunk.Body.KINEMATIC

    def paintEvent(self, event):
        p = QPainter(self)

        p.drawPixmap(0, 0, self.W, self.H, self.background)

        for body, color in ((self.ball, Qt.GlobalColor.red),
                            (self.batte, Qt.GlobalColor.darkYellow)):
            p.save()

            cx = body.position.x
            cy = self.H - body.position.y

            p.translate(cx, cy)

            angle_deg = -body.angle * 180.0 / math.pi
            p.rotate(angle_deg)

            p.setBrush(color)
            p.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

            p.setBrush(Qt.GlobalColor.white)
            p.drawEllipse(self.radius - 5, -5, 10, 10)

            p.restore()