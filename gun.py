import math
from random import choice
import random
import pygame

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1750
HEIGHT = 1030


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=900):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.t = 0

    #def __del__(self):


    def move(self):
        g = 0.01
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.t += 1
        self.vy = self.vy - self.t * g
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME

        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5

        if distance > (self.r + obj.r):
            return False
        else:
            return True


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.dx = 1
        self.dy = 1
        self.dX = 0
        self.dY = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) / 2
        new_ball.vy = - self.f2_power * math.sin(self.an) / 2
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.tan((event.pos[1] - 450) / (event.pos[0] - 20))
            # self.an = (900 - event.pos[1]) / (event.pos[0] - 20)
            self.dx = event.pos[0] - 20
            self.dy = 900 - event.pos[1]
            self.dX = 100 * self.dx / (self.dx ** 2 + self.dy ** 2) ** 0.5
            self.dY = 100 * self.dy / (self.dx ** 2 + self.dy ** 2) ** 0.5
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, [40, 900], [40 + self.dX / 5 + self.dX * self.f2_power / 100,
                                                         900 - self.dY / 5 - self.dY * self.f2_power / 100], 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 0
        self.color = RED
        self.points = 0
        self.live = 1
        self.xSpeed = 0
        self.ySpeed = 0

    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(100, 1700)
        self.y = random.randint(100, 900)
        self.r = random.randint(10, 50)
        self.xSpeed = random.randint(-2, 2)
        self.ySpeed = random.randint(-2, 2)
        self.live = True

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
target.new_target()

while not finished:
    screen.fill(WHITE)
    gun.draw()

    target.draw()

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
            b.move()
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()

    gun.power_up()
pygame.quit()