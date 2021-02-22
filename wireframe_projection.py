import pygame, time, math
pygame.init()

class Coords():
    x = 0
    y = 0
    z = 0
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

class Line():
    coords1 = None
    coords2 = None
    def __init__(self, c1, c2):
        self.coords1 = c1
        self.coords2 = c2

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def do_math(left_right_angle, up_down_angle, coords):
    if left_right_angle == 0:
        return Coords(coords.x, coords.y, coords.z)
    if left_right_angle == 90:
        return Coords(-coords.y, coords.x, coords.z)
    if left_right_angle == 180:
        return Coords(-coords.x, -coords.y, coords.z)
    if left_right_angle == 270:
        return Coords(coords.y, -coords.x, coords.z)

    b = coords.x / cos(90 - left_right_angle) - cos(left_right_angle) * (coords.x / tan(left_right_angle) - coords.y)
    a = (coords.x / cos(90 - left_right_angle) - b) * tan(left_right_angle)
    #for 3d, previous operations are enough for 2d
    b = coords.z / cos(up_down_angle) - cos(90 - up_down_angle) * (tan(up_down_angle) * coords.z - b)
    c = (coords.z / cos(up_down_angle) - b) / tan(90 - up_down_angle)
    return Coords(a, b, c)

def convert_to_display(coords):
    return (coords.x + 200, 200 - coords.z)

def draw_line(screen, color, line, left_right_angle, up_down_angle):
    pygame.draw.line(screen, color, convert_to_display(do_math(left_right_angle, up_down_angle, line.coords1)), convert_to_display(do_math(left_right_angle, up_down_angle, line.coords2)))

screen = pygame.display.set_mode((400, 400))
screen.fill('white')

lines = [
        Line(Coords(100, 100,), Coords(100, -100)),
        Line(Coords(100, -100), Coords(-100, -100)),
        Line(Coords(-100, -100), Coords(-100, 100)),
        Line(Coords(-100, 100), Coords(100, 100))
        ]

sqare = [
        Line(Coords(50, 50), Coords(50, 100)),
        Line(Coords(50, 100), Coords(100, 100)),
        Line(Coords(100, 100), Coords(100, 50)),
        Line(Coords(100, 50), Coords(50, 50)),
        ]

triangle = [
        Line(Coords(0, 0, 0), Coords(100, 0, 0)),
        Line(Coords(100, 0, 0), Coords(0, 0, 100)),
        Line(Coords(-100, 0, 0), Coords(0, 0, 100)),
        Line(Coords(0, 0, 50), Coords(0, 0, 0)),
        Line(Coords(0, 0, 50), Coords(0, 50, 50))
        ]

cube = [
        Line(Coords(0, 0, 0), Coords(0, 100, 0)),
        Line(Coords(0, 100, 0), Coords(100, 100, 0)),
        Line(Coords(100, 100, 0), Coords(100, 0, 0)),
        Line(Coords(100, 0, 0), Coords(0, 0, 0)),
        Line(Coords(0, 0, 0), Coords(0, 0, 100)),
        Line(Coords(0, 100, 0), Coords(0, 100, 100)),
        Line(Coords(100, 100, 0), Coords(100, 100, 100)),
        Line(Coords(100, 0, 0), Coords(100, 0, 100)),
        Line(Coords(0, 0, 100), Coords(0, 100, 100)),
        Line(Coords(0, 100, 100), Coords(100, 100, 100)),
        Line(Coords(100, 100, 100), Coords(100, 0, 100)),
        Line(Coords(100, 0, 100), Coords(0, 0, 100)),
        ]

up_down_angle = 0
left_right_angle = 0
last_up_down_angle = up_down_angle
last_left_right_angle = left_right_angle
while True:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        left_right_angle += 1
    elif pressed[pygame.K_LEFT]:
        left_right_angle -= 1
    elif pressed[pygame.K_UP]:
        up_down_angle -= 1
    elif pressed[pygame.K_DOWN]:
        up_down_angle += 1
    
    if left_right_angle <= -1:
        left_right_angle += 359
    elif left_right_angle >= 360:
        left_right_angle -= 360
    elif up_down_angle < 0:
        up_down_angle = 0
    elif up_down_angle > 180:
        up_down_angle = 180

    if left_right_angle != last_left_right_angle or up_down_angle != last_up_down_angle:
        screen.fill('white')
        print('left_right_angle : {}, up_down_angle : {}'.format(left_right_angle, up_down_angle))
        for line in cube:
            draw_line(screen, 'black', line, left_right_angle, up_down_angle)

        pygame.display.flip()
        time.sleep(.07)
        last_left_right_angle = left_right_angle
        last_up_down_angle = up_down_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
