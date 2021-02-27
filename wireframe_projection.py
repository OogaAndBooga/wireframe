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
    new_coords = Coords(coords.x, coords.y, coords.z) #new_coords are used in caculations instead, thats why they are assigned a value
    
    if left_right_angle == 0:
        new_coords = Coords(coords.x, coords.y, coords.z)
    elif left_right_angle == 90:
        new_coords = Coords(-coords.y, coords.x, coords.z)
    elif left_right_angle == 180:
        new_coords = Coords(-coords.x, -coords.y, coords.z)
    elif left_right_angle == 270:
        new_coords = Coords(coords.y, -coords.x, coords.z)
    else:
        new_coords.y = coords.x / cos(90 - left_right_angle) - cos(left_right_angle) * (coords.x / tan(left_right_angle) - coords.y)
        new_coords.x = (coords.x / cos(90 - left_right_angle) - new_coords.y) * tan(left_right_angle)
    
    #previous operations are enough for 2d, comment out the rest and change convert_to_display() for 2d
    if up_down_angle == 0:
       new_coords = Coords(new_coords.x, new_coords.z, -new_coords.y)
    elif up_down_angle == 90:
       pass # its all fine, nothing needs to change
    elif up_down_angle == 180:
       new_coords = Coords(new_coords.x, -new_coords.z, new_coords.y)
    else:
       new_coords.y = coords.z / cos(up_down_angle) - cos(90 - up_down_angle) * (tan(up_down_angle) * coords.z - new_coords.y)
       new_coords.z = (coords.z / cos(up_down_angle) - new_coords.y) * tan(90 - up_down_angle)

    return new_coords

def convert_to_display(coords, xshift, yshift):
    return (coords.x + 200 + xshift, 200 - coords.z + yshift)

def draw_line(screen, color, line, left_right_angle, up_down_angle, xshift = 0, yshift = 0):
    pygame.draw.line(screen, color, convert_to_display(do_math(left_right_angle, up_down_angle, line.coords1), xshift, yshift), convert_to_display(do_math(left_right_angle, up_down_angle, line.coords2), xshift, yshift))

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

pyramidh = 200
pyramid = [
        Line(Coords(100, 100, 0), Coords(100, -100, 0)),
        Line(Coords(100, -100, 0), Coords(-100, -100, 0)),
        Line(Coords(-100, -100, 0), Coords(-100, 100, 0)),
        Line(Coords(-100, 100, 0), Coords(100, 100 ,0)),
        Line(Coords(100, 100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(100, -100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(-100, -100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(-100, 100, 0), Coords(0, 0, pyramidh))
        ]

axis = [
        Line(Coords(0, 0, 0), Coords(20, 0, 0)),
        Line(Coords(0, 0, 0), Coords(0, 20, 0)),
        Line(Coords(0, 0, 0), Coords(0, 0, 20))
        ]

up_down_angle = 90
left_right_angle = 0
last_up_down_angle = up_down_angle
last_left_right_angle = left_right_angle

rate_of_turn = 2
a = 0
observer = Coords(0, 100, 0)

while True:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        left_right_angle += rate_of_turn
    elif pressed[pygame.K_LEFT]:
        left_right_angle -= rate_of_turn
    elif pressed[pygame.K_UP]:
        up_down_angle -= rate_of_turn
    elif pressed[pygame.K_DOWN]:
        up_down_angle += rate_of_turn
    
    if left_right_angle <= -1:
        left_right_angle += 360
    elif left_right_angle >= 360:
        left_right_angle -= 360
    elif up_down_angle < 0:
        up_down_angle = 0
    elif up_down_angle > 180:
        up_down_angle = 180

    if left_right_angle != last_left_right_angle or up_down_angle != last_up_down_angle:
        screen.fill('white')
        new_observer = do_math(left_right_angle, up_down_angle, observer)
        print('left_right_angle : {}, up_down_angle : {}'.format(left_right_angle, up_down_angle))
        for line in pyramid:
            draw_line(screen, 'black', line, left_right_angle, up_down_angle, observer.x + new_observer.x, 0)
        draw_line(screen, 'red', axis[0], left_right_angle, up_down_angle, -150, 150)
        draw_line(screen, 'green', axis[1], left_right_angle, up_down_angle, -150, 150)
        draw_line(screen, 'blue', axis[2], left_right_angle, up_down_angle, -150, 150)

        pygame.display.flip()
        time.sleep(.1)
        last_left_right_angle = left_right_angle
        last_up_down_angle = up_down_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
