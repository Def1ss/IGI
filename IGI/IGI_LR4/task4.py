"""
Task 4: Isosceles trapezoid with OOP (with abstract class)
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from abc import ABC, abstractmethod


class ShapeColor:
    """Class for shape color with property"""
    
    def __init__(self, color="blue"):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class GeometricShape(ABC):
    """Abstract base class for all geometric shapes"""
    
    shape_type = "Geometric Shape"
    
    @abstractmethod
    def area(self):
        """Calculate area of the shape"""
        pass
    
    @abstractmethod
    def __str__(self):
        """String representation of the shape"""
        pass


class IsoscelesTrapezoid(GeometricShape):
    """Isosceles trapezoid class inheriting from GeometricShape"""
    
    shape_type = "Isosceles Trapezoid"

    def __init__(self, a, b, h, color="blue"):
        self.a = float(a)   # lower base
        self.b = float(b)   # upper base
        self.h = float(h)   # height
        self._color = ShapeColor(color)

    @property
    def color(self):
        return self._color.color

    @color.setter
    def color(self, value):
        self._color.color = value

    def area(self):
        """Calculate area of trapezoid"""
        return (self.a + self.b) * self.h / 2

    def perimeter(self):
        """Calculate perimeter of trapezoid"""
        side = math.sqrt(self.h ** 2 + ((self.a - self.b) / 2) ** 2)
        return self.a + self.b + 2 * side

    def __str__(self):
        """Return formatted string with shape parameters, color and area"""
        return "{}: a={}, b={}, h={}, color={}, area={:.2f}".format(
            self.shape_type, self.a, self.b, self.h, self.color, self.area()
        )

    def draw(self, label="", save_path=None):
        """Draw the trapezoid with given label and save to file"""
        fig, ax = plt.subplots(figsize=(8, 6))

        # Vertices of isosceles trapezoid (centered at origin)
        x = [-self.a / 2, self.a / 2, self.b / 2, -self.b / 2]
        y = [-self.h / 2, -self.h / 2, self.h / 2, self.h / 2]

        poly = patches.Polygon(
            list(zip(x, y)), 
            closed=True, 
            facecolor=self.color, 
            edgecolor='black', 
            linewidth=2
        )
        ax.add_patch(poly)

        if label:
            ax.text(0, -self.h / 2 - 0.3, label, ha='center', fontsize=12)

        ax.set_xlim(-max(self.a, self.b) / 2 - 1, max(self.a, self.b) / 2 + 1)
        ax.set_ylim(-self.h / 2 - 1, self.h / 2 + 1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(self.shape_type)

        if save_path:
            plt.savefig(save_path)
        plt.show()


def validate_positive(value, name):
    """Validate that value is positive"""
    try:
        val = float(value)
        if val <= 0:
            print(f"Error: {name} must be positive")
            return None
        return val
    except ValueError:
        print(f"Error: Invalid {name} (must be a number)")
        return None


def main():
    print("\n=== ISOSCELES TRAPEZOID ===")
    
    # Input with validation
    a = validate_positive(input("Enter lower base (a): "), "lower base")
    if a is None:
        return
    
    b = validate_positive(input("Enter upper base (b): "), "upper base")
    if b is None:
        return
    
    h = validate_positive(input("Enter height (h): "), "height")
    if h is None:
        return
    
    color = input("Enter color (blue/red/green/yellow): ") or "blue"
    label = input("Enter text label: ")
    
    # Create trapezoid object
    trap = IsoscelesTrapezoid(a, b, h, color)
    
    # Display shape info using __str__
    print("\n" + str(trap))
    
    # Demonstrate color change
    if input("\nChange color? (y/n): ").lower() == 'y':
        new_color = input("Enter new color: ")
        trap.color = new_color
        print(f"New color: {trap.color}")
        print(str(trap))
    
    # Draw shape
    if input("\nDraw shape? (y/n): ").lower() == 'y':
        trap.draw(label, "trapezoid.png")
        print("Shape saved to trapezoid.png")


