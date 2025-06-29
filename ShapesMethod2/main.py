from .PackShapesMethod2 import (
    Point, 
    Line, 
    Shape, 
    Rectangle, 
    Square, 
    Triangle, 
    EquilateralTriangle, 
    IsoscelesTriangle, 
    Tri_Rectangle, 
    ScaleneTriangle
)

def main():
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print(f"\nPunto 1: {p1}")
    print(f"Punto 2: {p2}")

    linea = Line(p1, p2)
    print(f"\nLínea: {linea}")
    print(f"Longitud de la línea: {linea.compute_length():.2f}")
    print(f"Pendiente de la línea: {linea.compute_slope():.2f}")
    
    rect = Rectangle(10, 5, Point(2, 2))
    print("\nRectángulo:")
    print(f"Área: {rect.compute_area()}")
    print(f"Perímetro: {rect.compute_perimeter()}")
    rect.print_corners()

if __name__ == "__main__":
    main()
