from .PackShapesMethod1 import (Point, Line, Shape, Rectangle, Square, Triangle, EquilateralTriangle, IsoscelesTriangle, Tri_Rectangle, ScaleneTriangle)

def main():

    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print(f"\nPoint 1: {p1}")
    print(f"Point 2: {p2}")
    
    linea = Line(p1, p2)
    print(f"\nLine: {linea}")
    print(f"Length of the line: {linea.compute_length():.2f}")
    print(f"Slope of the line: {linea.compute_slope():.2f}")

    rect = Rectangle(10, 5, Point(2, 2))
    print("\nRectangle:")
    print(f"Área: {rect.compute_area()}")
    print(f"Perímeter: {rect.compute_perimeter()}")
    rect.print_corners()

if __name__ == "__main__":
    main()
