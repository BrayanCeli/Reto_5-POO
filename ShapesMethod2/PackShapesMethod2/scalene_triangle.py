from .triangle import Triangle

class ScaleneTriangle(Triangle):
    def __init__(self, point1, point2, point3):
        super().__init__(point1, point2, point3)
        if self.type == "equilatero" or self.type == "isosceles":
            raise ValueError("Los puntos deben ser de un triángulo escaleno")