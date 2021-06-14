import pygame
import math
import time

#creating display and variables for draw()
pygame.init()
screen = pygame.display.set_mode((400, 400))
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

    xzline = None
    yzline = None

    def __init__(self, c1, c2):
        self.coords1 = c1
        self.coords2 = c2
        if c2.x != c1.x: #condition for line perpendicular to x-axis
            self.slope = (c2.y - c1.y) / (c2.x - c1.x)
            self.yIntersect = c1.y - c1.x * self.slope
        else:
            self.slope = None #slope is already None, but imma set it again
    def __repr__(self):
        return('coords1 : {}\ncoords2 : {}'.format(self.coords1, self.coords2))

    def get_xzline(self):
        return Line(Coords(self.coords1.x, self.coords1.z), Coords(self.coords2.x, self.coords2.z))
    def get_yzline(self):
        return Line(Coords(self.coords1.y, self.coords1.z), Coords(self.coords2.y, self.coords2.z))

    def graph(self, x): #you shouldnt call it if the line is perpendicular to the x-axis
        return self.slope * x + self.yIntersect
    def threeDimensionalGraph(self, x):
        return Coords(x, self.graph(x), self.get_xzline().graph(x))

class Triangle():
    side1 = None
    side2 = None
    side3 = None
    #line1 and coords1 contain all 3 points, used in obstruct() to define the inside of a triangle(and also usefull for get_semiplane())
    coords1 = None
    coords2 = None
    coords3 = None

    #for the graph function
    xyline = None
    yzline = None # just used for its graph function
    xzline = None

    def __init__(self, l1, l2, l3):
        if isinstance(l1, Line):
            self.side1 = l1
            self.side2 = l2
            self.side3 = l3
            #its ugly but it wotks(i dont know how to make the code better)
            #also, i think it figures the coordsN opposite to lineN(i cant remember what it does)
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
        elif isinstance(l1, Coords):
            self.coords1 = c1
            self.coords2 = c2
            self.coords3 = c3

            self.side1 = Line(c2, c3)
            self.side2 = Line(c1, c3)
            self.side3 = Line(c1, c2)

        #find xyline
        side1 = get_xyplane_intersection(self.side1)
        side2 = get_xyplane_intersection(self.side2)
        side3 = get_xyplane_intersection(self.side3)
        print("side1, side2, side3", bool(side1), bool(side2), bool(side3))

        if side1 is None and side2 is None and side3 is None:
            self.xyline = None #this way, self.graph() will know if the plane is paralell to xy-plane
        elif side1 is not None:
            if side2 is not None:
                self.xyline = Line(get_xyplane_intersection(self.side1), get_xyplane_intersection(self.side2))
            else:
                self.xyline = Line(get_xyplane_intersection(self.side1), get_xyplane_intersection(self.side3))
        else:
            self.xyline = Line(get_xyplane_intersection(self.side2), get_xyplane_intersection(self.side3))

        #find coords that arent incuded in xyplane
        if self.coords1.z != 0:
            notxycoords = self.coords1
        elif self.coords2.z != 0:
            notxycoords = self.coords2
        elif self.coords3.z != 0:
            notxycoords = self.coords3

        #find yzline(yzline.slope is important) or xzline
        if self.xyline is not None:
            if self.xyline.slope is not None:
                self.yzline = Line(Coords(notxycoords.y, notxycoords.z), Coords(self.xyline.graph(notxycoords.x) , 0))
            else: # in this case, will will find xz-line
                self.xzline = Line(Coords(notxycoords.x, notxycoords.z), Coords(notxycoords.x, 0))

    def graph(self, coords):
        if self.xyline is None: #plane is paralell to xy-plane
            print('plane is paralell')
            return self.coords1.z
        elif self.yzline.slope is None: #plane is perpendicular to xy-plane
            print('plane in parpendicular')
            return None
        else:
            if self.xzline is None:
                print('plane is normal')
                y = self.xyline.graph(coords.x)
                print('y = {}'.format(y))
                self.yzline.yIntersect = 0
                self.yzline.yIntersect = -self.yzline.graph(y) #get yzline for slope
                print('yzline yintersect {}'.format(self.yzline.yIntersect))
                return self.yzline.graph(coords.y)
            else:
                print('plane has xyline perpendicualr to x-axis')
                return self.xzline.graph(coords.x)

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
    intersection = get_graph_intersection(line1, line2)
    if intersection is None:
        return None

    #checks if intersection happens on segment(i dont know why removing the y check made  it work(probabley returning an intersection when there was not))
    def is_in_between(a, b, c):
        return b <= a <= c or b >= a >= c
    if is_in_between(intersection.x, line1.coords1.x, line1.coords2.x) and is_in_between(intersection.x, line2.coords1.x, line2.coords2.x):
        return intersection
    else:
        return None

def get_graph_intersection(line1, line2):
    if line1.slope is not None and line2.slope is not None:
        if line1.slope != line2.slope: #make sure lines are not paralell
            x = (line2.yIntersect - line1.yIntersect) / (line1.slope - line2.slope)
            y = line1.graph(x)
            return Coords(x, y)
        else:
            return None
    elif line1.slope is not None and line2.slope is None:
        x = line2.coords1.x
        y = line1.graph(x)
        return Coords(x, y)
    elif line1.slope is None and line2.slope is not None:
        x = line1.coords1.x
        y = line2.graph(x)
        return Coords(x, y)
    elif line1.slope is None and line2.slope is None:
        return None

def get_xyplane_intersection(line):
    if line.coords1.z == line.coords2.z:
        return None
    elif line.coords1.x != line.coords2.x: #normal intersection
        intersection = get_graph_intersection(line.get_xzline(), Line(Coords(0, 0), Coords(1, 0)))
        return Coords(intersection.x, line.graph(intersection.x))
    elif line.coords1.y != line.coords2.y: # x is constant, use yzline to get y when z=0
        intersection = get_graph_intersection(line.get_yzline(), Line(Coords(0, 0), Coords(1, 0)))
        return Coords(line.coords1.x, intersection.x)
    elif line1.coords1.x == line: #line is perpendicular to xy-plane
        return Coords(line.coords1.x, line.coords1.y)


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
        print('completed obstructed')
        return [] #the line is obstructed completley
    elif is_inside(line.coords1, triangle):
        print('coords 1 inside')
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            print(side, line, intersection, '\n')
            if intersection:
                print('partley bostructed')
                return [Line(line.coords2, intersection)]
    elif is_inside(line.coords2, triangle):
        print('coords2 inside')
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            if intersection:
                print('partley obstructed')
                return [Line(line.coords1, intersection)]
    else:
        print('this statment got triggered (intel inside) (no coords inside)')
        new_lines = []
        for side in [triangle.side1, triangle.side2, triangle.side3]:
            intersection = get_intersection(side, line)
            if intersection:
                #finds the non-obstructed linechr
                if get_semiplane(line.coords1, side) != get_semiplane(triangle.get_opposite_coords(side), side):
                    new_lines.append(Line(line.coords1, intersection))
                else:
                    new_lines.append(Line(line.coords2, intersection))
        #make sure to retunr the original line if not obstructed
        if new_lines != []:
            print('middle obstruced')
            return new_lines
        else:
            print('not obstructed')
            return [line]

    print('ERRRRROR BIG FAT ERROR, IT RETURNS nothing. NOTHING!!!')


#return coords relative to the display plane, {relative to the display plane} x, y plane coords z distance from plane
def convert_to_display(data, xshift = 0, yshift = 0):
    if isinstance(data, Coords):
        return Coords(data.x + screen.get_width() / 2 + xshift, screen.get_height() / 2 - data.z + yshift, data.y)
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
    elif isinstance(data, Triangle):
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
        Line(Coords(0, 0, 0), Coords(0, 0, 20))
        ]

up_down_angle = 90
left_right_angle = 0
last_up_down_angle = up_down_angle
last_left_right_angle = left_right_angle

#TODO remove this
#pygame.quit()

c1 = Coords(-100, 100, 100)
c2 = Coords(100, 100, 100)
c3 = Coords(0, 0, 100)
c4= Coords(100, 0)
line1 = Line(c1, c2)
line2 = Line(c3, c4)
plane = Triangle(c1, c2, c3)
pygame.quit()
#raise KeyboardInterrupt("muhahaha")

rate_of_turn = 2
while True:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        left_right_angle -= rate_of_turn
    if pressed[pygame.K_LEFT]:
        left_right_angle += rate_of_turn
    if pressed[pygame.K_UP]:
        up_down_angle -= rate_of_turn
    if pressed[pygame.K_DOWN]:
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
        print(triangle.coords1)
        print(triangle.coords2)
        print(triangle.coords3, '\n')

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