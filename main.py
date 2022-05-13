# Source video : https://youtu.be/WTLPmUHTPqo

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)


class Planet:
    """Astronomical Unit"""
    AU = 149.6e6 * 1000
    """Acceleration of gravity"""
    G = 6.67428e-11
    """1 AU -> 100px"""
    SCALE = 250 / AU
    """1 day"""
    TIME_STEP = 3600 * 24

    def __init__(self, x: float, y: float, radius: float, color: tuple, mass: int):
        self.x = x
        self.y = y
        self.radius = radius,
        self.color = color,
        self.mass = mass

        """If it's the Sun"""
        self.sun = False

        self.distance_to_sun = 0
        self.orbit = []

        """Velocity"""
        self.x_vel = 0
        self.y_vel = 0

    def draw(self):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)

        # FIXME : Radius compris comme un tuple
        pygame.draw.circle(WIN, self.color, (x, y), self.radius[0])

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.attraction(planet)
            total_fx += force_x
            total_fy += force_y

        self.x_vel += total_fx / self.mass * self.TIME_STEP
        self.y_vel += total_fy / self.mass * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP

        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        """60 FPS"""
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw()

        pygame.display.update()

    pygame.quit()


main()
