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
square_pyramid = [
        Line(Coords(100, 100, 0), Coords(100, -100, 0)),
        Line(Coords(100, -100, 0), Coords(-100, -100, 0)),
        Line(Coords(-100, -100, 0), Coords(-100, 100, 0)),
        Line(Coords(-100, 100, 0), Coords(100, 100 ,0)),
        Line(Coords(100, 100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(100, -100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(-100, -100, 0), Coords(0, 0, pyramidh)),
        Line(Coords(-100, 100, 0), Coords(0, 0, pyramidh))
        ]

triangle_pyramid = [
        Line(Coords(-100, 0, 0), Coords(100, 0, 0)),
        Line(Coords(100, 0, 0), Coords(0, 200, 0)),
        Line(Coords(0, 200, 0), Coords(-100, 0, 0)),
        Line(Coords(-100, 0, 0), Coords(0, 0, 200)),
        Line(Coords(100, 0, 0), Coords(0, 0, 200)),
        Line(Coords(0, 200, 0), Coords(0, 0, 200)),
        ]
