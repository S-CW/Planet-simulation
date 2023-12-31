import pygame
import math


pygame.init()

# initialization
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# variables
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 16)

# Unit used in meters
# Physics formula
    # F = ma (kgms⁻²)
    # Velocity unit ms⁻¹
class Planet:
    AU = 149.6e6 * 1000 # 149.6 million km, in meters.
    G = 6.67428e-11
    SCALE = 250 / AU    # 1AU = 100 pixels, smaller AU makes planets closer to sun
    TIMESTEP = 3600 * 24    # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        planet_x = self.x * self.SCALE + WIDTH / 2
        planet_y = self.y * self.SCALE + HEIGHT / 2

        # get the correct scale based on window size
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (planet_x, planet_y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (planet_x - distance_text.get_width()/2, planet_y + 15))


    def attraction(self, other_planet):
        other_planet_x, other_planet_y = other_planet.x, other_planet.y
        distance_x = other_planet_x - self.x
        distance_y = other_planet_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other_planet.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other_planet.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0

        # calculate the total force combine from other planets
        for planet in planets:
            if self == planet:
                continue
            
            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y
        
        self.x_vel += total_force_x / self.mass * self.TIMESTEP  # a = F / m
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    # Add new planets here on next line

    planets = [sun, earth, mars, mercury, venus]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        SCREEN.fill("black")

        for planet in planets:
            planet.update_position(planets)
            planet.draw(SCREEN)



        pygame.display.update()
        clock.tick(60)
    pygame.quit()

main()