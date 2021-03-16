import pygame, time, math
pygame.init()

size = (width, height) = (400, 400) #also gets used in convert_to_display function
screen = pygame.display.set_mode(size)
screen.fill('white')

class Coords():
    x = 0
    y = 0
    z = 0
    pygame_format = None
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
        self.pygame_format = (x, y)
    def __repr__(self):
        return('x : {}, y : {}, z : {}'.format(round(self.x, 2), round(self.y, 2), round(self.z, 2)))

class Line():
    coords1 = None
    coords2 = None
    def __init__(self, c1, c2):
        self.coords1 = c1
        self.coords2 = c2
    def __repr__(self):
        return('line1 : {}\nline2 : {}'.format(self.coords1, self.coords2))

class Polygon():
    line1 = None
    line2 = None
    line3 = None
    def __init__(self, l1, l2, l3):
        self.line1 = l1
        self.line2 = l2
        self.line3 = l3

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def do_math_coords(left_right_angle, up_down_angle, coords):
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

def do_math_line(left_right_angle, up_down_angle, line):
    c1 = do_math_coords(left_right_angle, up_down_angle, line.coords1)
    c2 = do_math_coords(left_right_angle, up_down_angle, line.coords2)
    return Line(c1, c2)

def do_math_polygon(left_right_angle, up_down_angle, polygon):
    l1 = do_math_line(left_right_angle, up_down_angle, polygon.line1)
    l2 = do_math_line(left_right_angle, up_down_angle, polygon.line2)
    l3 = do_math_line(left_right_angle, up_down_angle, polygon.line3)
    return Polygon(l1, l2, l3)

def get_intersection(line1, line2):
    a1 = (line1.coords2.y - line1.coords1.y) / (line1.coords2.x - line1.coords1.x)
    b1 = line1.coords1.y - line1.coords1.x * a1

    a2 = (line2.coords2.y - line2.coords1.y) / (line2.coords2.x - line2.coords1.x)
    b2 = line2.coords1.y - line2.coords1.x * a2
    #this is the intersection
    x = (b2 - b1) / (a1 - a2)
    y = x * a2 + b2

    print('a1 : {}, b1 : {}'.format(a1, b1))
    print('a2 : {}, b2 : {}'.format(a2, b2))
    return(Coords(x,y))

#return coords relative to the display plane, {relative to the display plane} x, y plane coords z distance from plane
def convert_to_display(data, xshift = 0, yshift = 0):
    if isinstance(data, Coords):
        return Coords(data.x + width / 2 + xshift, height / 2 - data.z + yshift, data.y)
    elif isinstance(data, Line):
        return Line(convert_to_display(data.coords1, xshift, yshift), convert_to_display(data.coords2, xshift, yshift))
    elif isinstance(data, Polygon):
        line1 = convert_to_display(data.line1, xshift, yshift)
        line2 = convert_to_display(data.line2, xshift, yshift)
        line3 = convert_to_display(data.line3, xshift, yshift)
        return Polygon(line1, line2, line3)

        
### THE DRAW FUNCTIONS JUST DRAW, AND DONT PROCESS/CHANGE ANYTHING
### THEY JUST GET COORDS AND DRAW THEM

def draw_line(screen, color, line):
    pygame.draw.line(screen, color, line.coords1.pygame_format, line.coords2.pygame_format)

def draw_polygon(screen, color, polygon):
    draw_line(screen, color, polygon.line1)
    draw_line(screen, color, polygon.line2)
    draw_line(screen, color, polygon.line3)

#the test(for planes obstructing lines) format fill be a map with planes and lines
test_shape = {
'polygon' : Polygon(Line(Coords(-100, 0, 0), Coords(100, 0, 0)), Line(Coords(100, 0, 0), Coords(0, 0, 100)),Line(Coords(0, 0, 100), Coords(-100, 0, 0))),
'line' : Line(Coords(-200, 100, 50), Coords(200, 100, 50))
            }

axis = [
        Line(Coords(0, 0, 0), Coords(40, 0, 0)),
        Line(Coords(0, 0, 0), Coords(0, 40, 0)),
        Line(Coords(0, 0, 0), Coords(0, 0, 40))
        ]

up_down_angle = 90
left_right_angle = 0
last_up_down_angle = up_down_angle
last_left_right_angle = left_right_angle

#TODO remove this
#pygame.quit()

rate_of_turn = 2
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
        print('left_right_angle : {}, up_down_angle : {}'.format(left_right_angle, up_down_angle))

        ## the draw function just draw, it also needs do pass trough : do_math, convert_to display(returns a tuple for pygame's draw function)
        polygon = test_shape['polygon']
        line = test_shape['line']

        line = convert_to_display(do_math_line(left_right_angle, up_down_angle, line))
        polygon = convert_to_display(do_math_polygon(left_right_angle, up_down_angle, polygon))

        draw_polygon(screen, 'green', polygon)
        draw_line(screen, 'grey', line)

        #idk

        draw_line(screen, 'red', convert_to_display(do_math_line(left_right_angle, up_down_angle, axis[0]), -150, 150))
        draw_line(screen, 'green', convert_to_display(do_math_line(left_right_angle, up_down_angle, axis[1]), -150, 150))
        draw_line(screen, 'blue', convert_to_display(do_math_line(left_right_angle, up_down_angle, axis[2]), -150, 150))

        pygame.display.flip()
        time.sleep(.1)
        last_left_right_angle = left_right_angle
        last_up_down_angle = up_down_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()