import time
import math
import pygame

#creating display and variables for draw()
pygame.init()
size = (width, height) = (400, 400)
screen = pygame.display.set_mode(size)
screen.fill('white')

class Coords():
    x = 0
    y = 0
    z = 0
    pygame_format = None #This is for passing the coords to pygame function, it accepts a tuple : (x, y)

    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
        self.pygame_format = (x, y)

    def __eq__(self, other):
        if(self.x == other.x and self.y == other.y and self.z == other.z):
            return True
        else:
            return False

    def __repr__(self):
        return('x : {}, y : {}, z : {}'.format(round(self.x, 2), round(self.y, 2), round(self.z, 2)))

class Line():
    coords1 = None
    coords2 = None
    slope = None
    yIntersect = None

    def graph(self, x): #you shouldnt call it if the line is perpendicular to the x-axis
        if self.slope != None:
            return self.slope * x + self.yIntersect

    def __init__(self, c1, c2):
        self.coords1 = c1
        self.coords2 = c2
        if c2.x - c1.x != 0: #condition for line perpendicular to x-axis
            self.slope = (c2.y - c1.y) / (c2.x - c1.x)
            self.yIntersect = c1.y - c1.x * self.slope
        else:
            self.slope = None #slope is already None, but imma set it again

    def __repr__(self):
        return('coords1 : {}\ncoords2 : {}'.format(self.coords1, self.coords2))

class Triangle():
    side1 = None
    side2 = None
    side3 = None
    #line1 and coords1 contain all 3 points, used in obstruct() to define the inside of a triangle(and also usefull for get_semiplane())
    coords1 = None
    coords2 = None
    coords3 = None
    
    def __init__(self, l1, l2, l3):
        self.side1 = l1
        self.side2 = l2
        self.side3 = l3

        #it looks ugly(i dont know how to make the code prettier)
        if l1.coords1 == l2.coords1 or l1.coords2 == l2.coords1:
            self.coords1 = l2.coords2
        else:
            self.coords1 = l2.coords1
        if l2.coords1 == l3.coords1 or l2.coords2 == l3.coords1:
            self.coords2 = l3.coords2
        else:
            self.coords2 = l3.coords1
        if l3.coords1 == l1.coords1 or l3.coords2 == l1.coords1:
            self.coords3 = l1.coords2
        else:
            self.coords3 = l1.coords1
    
    def get_opposite_coords(self, side):
        if side == self.side1:
            return self.coords1
        elif side == self.side2:
            return self.coords2
        elif side == self.side3:
            return self.coords3


    # def __repr__(self):
    #     s = self
    #     return('line1, coords1 : {}, {}\nline2, coords2 : {}, {}\nline3, coords3 : {}, {}'.format(s.line1, s.coords1, s.line2, s.coords2, s.line3, s.coords3))

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
    
    elif isinstance(data, Triangle):
        l1 = do_math(left_right_angle, up_down_angle, data.side1)
        l2 = do_math(left_right_angle, up_down_angle, data.side2)
        l3 = do_math(left_right_angle, up_down_angle, data.side3)
        return Triangle(l1, l2, l3)


def get_intersection(line1, line2):
    if line1.slope is not None and line2.slope is not None:
        if line1.slope != line2.slope: #if true, lines are  paralel
            x = (line2.yIntersect - line1.yIntersect) / (line1.slope - line2.slope)
            y = line1.graph(x)
        else:
            return None
    elif line1.slope is not None and line2.slope is None:
        x = line2.coords1.x
        y = line1.graph(x)
    elif line1.slope is None and line2.slope is not None:
        x = line1.coords1.x
        y = line2.graph(x)
    elif line1.slope is None and line2.slope is None:
        return None
        #i have no ideea on  how to do this(i think this is fine)(if they are parralel they cant intersect)

    #checks if intersection happens on segment
    on_line1_x = line1.coords1.x <= x <= line1.coords2.x or line1.coords1.x >= x >= line1.coords2.x
    on_line1_y = line1.coords1.y <= y <= line1.coords2.y or line1.coords1.y >= y >= line1.coords2.y
    on_line2_x = line2.coords1.x <= x <= line2.coords2.x or line2.coords1.x >= x >= line2.coords2.x
    on_line2_y = line2.coords1.y <= y <= line2.coords2.y or line2.coords1.y >= y >= line2.coords2.y
    if on_line1_x and on_line1_y and on_line2_x and on_line2_y:
        return(Coords(x,y))
    else:
        return None

def get_semiplane(coords, line):
    if line.slope is None:
        if coords.x >= line.coords1.x:
            return True
        else:
            return False
    else:
        if coords.y >= line.graph(coords.x):
            return True
        else:
            return False

def is_inside(coords, triangle):
    #triangle coords1 and line1 contan enough data to draw the triangle
    inside1 = get_semiplane(coords, triangle.side1) == get_semiplane(triangle.coords1, triangle.side1)
    inside2 = get_semiplane(coords, triangle.side2) == get_semiplane(triangle.coords2, triangle.side2)
    inside3 = get_semiplane(coords, triangle.side3) == get_semiplane(triangle.coords3, triangle.side3)
    if inside1 == inside2 == inside3:
        return True
    else:
        return False

def obstruct(line, triangle):
    if is_inside(line.coords1, triangle) and is_inside(line.coords2, triangle):
        return [] #the line is obstructed completley
    elif is_inside(line.coords1, triangle):
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            if intersection:
                return [Line(line.coords2, intersection)]
    elif is_inside(line.coords2, triangle):
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            if intersection:
                return [Line(line.coords1, intersection)]
    else:
        new_lines = []
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            if intersection:
                #finds the non-obstructed line
                if get_semiplane(line.coords1, side) != get_semiplane(triangle.get_opposite_coords(side), side):
                    new_lines.append(Line(line.coords1, intersection))
                else:
                    new_lines.append(Line(line.coords2, intersection))
        #make sure to retunr the original line if not obstructed
        if new_lines != []:
            return new_lines
        else:
            return [line]


#return coords relative to the display plane, {relative to the display plane} x, y plane coords z distance from plane
def convert_to_display(data, xshift = 0, yshift = 0):
    if isinstance(data, Coords):
        return Coords(data.x + width / 2 + xshift, height / 2 - data.z + yshift, data.y)
    elif isinstance(data, Line):
        return Line(convert_to_display(data.coords1, xshift, yshift), convert_to_display(data.coords2, xshift, yshift))
    elif isinstance(data, Triangle):
        line1 = convert_to_display(data.side1, xshift, yshift)
        line2 = convert_to_display(data.side2, xshift, yshift)
        line3 = convert_to_display(data.side3, xshift, yshift)
        return Triangle(line1, line2, line3)
        
### THE DRAW FUNCTIONS JUST DRAW, AND DONT PROCESS/CHANGE ANYTHING
### THEY JUST GET COORDS AND DRAW THEM
def draw(data, color):
    if isinstance(data, Line):
        pygame.draw.line(screen, color, data.coords1.pygame_format, data.coords2.pygame_format, 1)
    elif isinstance(data,Triangle):
        draw(data.side1, color)
        draw(data.side2, color)
        draw(data.side3, color)

#the test_shapez(for planes obstructing lines)
test_shapes = {
    'triangle' : Triangle(Line(Coords(-100, 0, 0), Coords(100, 0, 0)), Line(Coords(100, 0, 0), Coords(0, 0, 100)),Line(Coords(0, 0, 100), Coords(-100, 0, 0))),
    'line' : Line(Coords(-200, 100, 50), Coords(200, 100, 50))
    }

axis = [
        Line(Coords(0, 0, 0), Coords(20, 0, 0)),
        Line(Coords(0, 0, 0), Coords(0, 20, 0)),
        Line(Coords(0, 0, 0), Coords(0, 0, 2))
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

        ## the draw function just draws, it also needs do pass trough : do_math, convert_to display(returns a tuple for pygame's draw function)
        triangle = test_shapes['triangle']
        line = test_shapes['line']

        line = convert_to_display(do_math(left_right_angle, up_down_angle, line))
        triangle = convert_to_display(do_math(left_right_angle, up_down_angle, triangle))

        for l in obstruct(line, triangle):
            draw(l, 'black')
        draw(triangle, 'black')

        draw(convert_to_display(do_math(left_right_angle, up_down_angle, axis[0]), -150, 150), 'red')
        draw(convert_to_display(do_math(left_right_angle, up_down_angle, axis[1]), -150, 150), 'green')
        draw(convert_to_display(do_math(left_right_angle, up_down_angle, axis[2]), -150, 150), 'blue')

        pygame.display.flip()
        time.sleep(.1)
        last_left_right_angle = left_right_angle
        last_up_down_angle = up_down_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()