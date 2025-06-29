import math

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    
    def restart(self):
        self.x = 0
        self.y = 0
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, start=Point(), end=Point()):
        self.start = start
        self.end = end
    
    def compute_length(self):
        return math.sqrt((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)
    
    def compute_slope(self):
        if self.end.x == self.start.x:
            return float('inf')
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)
    
    def __str__(self):
        return f"Linea desde {self.start} hasta {self.end}"


class Shape:
    def __init__(self, center=Point()):
        self.center = center
    
    def compute_area(self):
        raise NotImplementedError("Las subclases deben implementar compute_area()")
    
    def compute_perimeter(self):
        raise NotImplementedError("Las subclases deben implementar compute_perimeter()")
    
    def compute_interference_point(self, point):
        raise NotImplementedError("Las subclases deben implementar compute_interference_point()")
    
    def compute_interference_line(self, line):
        raise NotImplementedError("Las subclases deben implementar compute_interference_line()")


class Rectangle(Shape):
    def __init__(self, width, height, center=Point()):
        super().__init__(center)
        self.width = width
        self.height = height
    
    def get_corners(self):
        half_w = self.width / 2
        half_h = self.height / 2
        return [
            Point(self.center.x + half_w, self.center.y + half_h),  
            Point(self.center.x - half_w, self.center.y + half_h),  
            Point(self.center.x - half_w, self.center.y - half_h),  
            Point(self.center.x + half_w, self.center.y - half_h)   
        ]
    
    def print_corners(self):
        corners = ["Top right", "Top left", "Bottom left", "Bottom right"]
        for name, point in zip(corners, self.get_corners()):
            print(f"{name}: {point}")
    
    def compute_area(self):
        return self.width * self.height
    
    def compute_perimeter(self):
        return 2 * (self.width + self.height)
    
    def compute_interference_point(self, point):
        corners = self.get_corners()
        min_x = min(p.x for p in corners)
        max_x = max(p.x for p in corners)
        min_y = min(p.y for p in corners)
        max_y = max(p.y for p in corners)
        return (min_x <= point.x <= max_x) and (min_y <= point.y <= max_y)
    
    def compute_interference_line(self, line):
        return (self.compute_interference_point(line.start) or 
                self.compute_interference_point(line.end))


class Square(Rectangle):
    def __init__(self, side, center=Point()):
        super().__init__(side, side, center)
        self.side = side
    
    def set_side(self, value):
        if value <= 0:
            raise ValueError("Lado largo debe ser positivo")
        self.side = value
        self.width = value
        self.height = value


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


class EquilateralTriangle(Triangle):
    def __init__(self, center, side_length):
        height = (math.sqrt(3) / 2) * side_length  
        p1 = Point(center.x, center.y + (2/3)*height)
        p2 = Point(center.x - side_length/2, center.y - (1/3)*height)
        p3 = Point(center.x + side_length/2, center.y - (1/3)*height)
        super().__init__(p1, p2, p3)
        self.side_length = side_length


class IsoscelesTriangle(Triangle):
    def __init__(self, base_center, base_length, height):
        p1 = Point(base_center.x - base_length/2, base_center.y - height/2)
        p2 = Point(base_center.x + base_length/2, base_center.y - height/2)
        p3 = Point(base_center.x, base_center.y + height/2)
        super().__init__(p1, p2, p3)
        self.base_length = base_length
        self.height = height


class Tri_Rectangle(Triangle):
    def __init__(self, right_angle_point, leg1, leg2):
        p1 = right_angle_point
        p2 = Point(p1.x + leg1, p1.y)
        p3 = Point(p1.x, p1.y + leg2)
        super().__init__(p1, p2, p3)
        self.leg1 = leg1
        self.leg2 = leg2


class ScaleneTriangle(Triangle):
    def __init__(self, point1, point2, point3):
        super().__init__(point1, point2, point3)
        if self.type == "equilatero" or self.type == "isosceles":
            raise ValueError("Los puntos deben ser de un triángulo escaleno")


if __name__ == "__main__":
