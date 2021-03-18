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
    slope = None
    yIntersect = None

    # def graph(self, x):
    #     if self.slope != None
    #         return self.slope * x + self.yIntersect
    #     else:
    #         return None

    def __init__(self, c1, c2):
        self.coords1 = c1
        self.coords2 = c2
        try:
            self.slope = (c2.y - c1.y) / (c2.x - c1.x)
            self.yIntersect = c1.y - c1.x * self.slope
        except(ZeroDivisionError):
            pass #slope is already None
    
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

def do_math(left_right_angle, up_down_angle, data):
    if isinstance(data, Coords):
        new_data = Coords(data.x, data.y, data.z) #new_data are used in caculations instead, thats why they are assigned a value
    
        if left_right_angle == 0:
            new_data = Coords(data.x, data.y, data.z)
        elif left_right_angle == 90:
            new_data = Coords(-data.y, data.x, data.z)
        elif left_right_angle == 180:
            new_data = Coords(-data.x, -data.y, data.z)
        elif left_right_angle == 270:
            new_data = Coords(data.y, -data.x, data.z)
        else:
            new_data.y = data.x / cos(90 - left_right_angle) - cos(left_right_angle) * (data.x / tan(left_right_angle) - data.y)
            new_data.x = (data.x / cos(90 - left_right_angle) - new_data.y) * tan(left_right_angle)
    
        #previous operations are enough for 2d, comment out the rest and change convert_to_display() for 2d
        if up_down_angle == 0:
            new_data = Coords(new_data.x, new_data.z, -new_data.y)
        elif up_down_angle == 90:
            pass # its all fine, nothing needs to change
        elif up_down_angle == 180:
            new_data = Coords(new_data.x, -new_data.z, new_data.y)
        else:
            new_data.y = data.z / cos(up_down_angle) - cos(90 - up_down_angle) * (tan(up_down_angle) * data.z - new_data.y)
            new_data.z = (data.z / cos(up_down_angle) - new_data.y) * tan(90 - up_down_angle)
        
        return new_data
    
    elif isinstance(data, Line):
        c1 = do_math(left_right_angle, up_down_angle, data.coords1)
        c2 = do_math(left_right_angle, up_down_angle, data.coords2)
        return Line(c1, c2)
    
    elif isinstance(data, Polygon):
        l1 = do_math(left_right_angle, up_down_angle, data.line1)
        l2 = do_math(left_right_angle, up_down_angle, data.line2)
        l3 = do_math(left_right_angle, up_down_angle, data.line3)
        return Polygon(l1, l2, l3)


# def do_math_line(left_right_angle, up_down_angle, line):
#     c1 = do_math_coords(left_right_angle, up_down_angle, line.coords1)
#     c2 = do_math_coords(left_right_angle, up_down_angle, line.coords2)
#     return Line(c1, c2)

# def do_math_polygon(left_right_angle, up_down_angle, polygon):
#     l1 = do_math_line(left_right_angle, up_down_angle, polygon.line1)
#     l2 = do_math_line(left_right_angle, up_down_angle, polygon.line2)
#     l3 = do_math_line(left_right_angle, up_down_angle, polygon.line3)
#     return Polygon(l1, l2, l3)

def get_intersection(line1, line2):
    if line1.slope is None:
        pass
    else:
        x = (line2.yIntersect - line1.yIntersect) / (line1.sleep - line2.slope)
        y = line1.graph(x)
    # a1 = (line1.coords2.y - line1.coords1.y) / (line1.coords2.x - line1.coords1.x)
    # b1 = line1.coords1.y - line1.coords1.x * a1

    # a2 = (line2.coords2.y - line2.coords1.y) / (line2.coords2.x - line2.coords1.x)
    # b2 = line2.coords1.y - line2.coords1.x * a2
    #   this is the intersection
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

def draw(screen, color, data):
    if isinstance(data, Line):
        pygame.draw.line(screen, color, data.coords1.pygame_format, data.coords2.pygame_format)
    elif isinstance(data, Polygon):
        draw(screen, color, data.line1)
        draw(screen, color, data.line2)
        draw(screen, color, data.line3)

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

        line = convert_to_display(do_math(left_right_angle, up_down_angle, line))
        polygon = convert_to_display(do_math(left_right_angle, up_down_angle, polygon))

        draw(screen, 'green', polygon)
        draw(screen, 'grey', line)

        #idk

        draw(screen, 'red', convert_to_display(do_math(left_right_angle, up_down_angle, axis[0]), -150, 150))
        draw(screen, 'green', convert_to_display(do_math(left_right_angle, up_down_angle, axis[1]), -150, 150))
        draw(screen, 'blue', convert_to_display(do_math(left_right_angle, up_down_angle, axis[2]), -150, 150))

        pygame.display.flip()
        time.sleep(.1)
        last_left_right_angle = left_right_angle
        last_up_down_angle = up_down_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()