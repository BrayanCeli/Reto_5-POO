import math
from .shape import Shape
from .point import Point
from .line import Line

class Triangle(Shape):
    def __init__(self, point1, point2, point3):
        super().__init__(self.compute_centroid([point1, point2, point3]))
        self.points = [point1, point2, point3]
        self.sides = [
            Line(point1, point2),
            Line(point2, point3),
            Line(point3, point1)
        ]
        self.side_lengths = [side.compute_length() for side in self.sides]
        self.type = self.determine_type()
    
    def determine_type(self):
        a, b, c = sorted(self.side_lengths)
        
        if not (a + b > c):
            raise ValueError("Triangulo no valido")
        
        if math.isclose(a, b) and math.isclose(b, c):
            return "equilatero"
        
        if math.isclose(a**2 + b**2, c**2):
            if math.isclose(a, b):
                return "isosceles_right"
            return "right"
        
        if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            return "isosceles"
        
        return "escaleno"
    
    def compute_perimeter(self):
        return sum(self.side_lengths)
    
    def compute_area(self):
        a, b, c = self.side_lengths
        s = self.compute_perimeter() / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    def compute_interference_point(self, point):
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(point, self.points[0], self.points[1])
        d2 = sign(point, self.points[1], self.points[2])
        d3 = sign(point, self.points[2], self.points[0])
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)