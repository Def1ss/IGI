"""
Task 4: Isosceles trapezoid with OOP
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class ShapeColor:
    def __init__(self, color="blue"):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class IsoscelesTrapezoid:
    shape_type = "Isosceles Trapezoid"

    def __init__(self, a, b, h, color="blue"):
        self.a = float(a)
        self.b = float(b)
        self.h = float(h)
        self._color = ShapeColor(color)

    @property
    def color(self):
        return self._color.color

    @color.setter
    def color(self, value):
        self._color.color = value

    def area(self):
        return (self.a + self.b) * self.h / 2

    def perimeter(self):
        side = math.sqrt(self.h ** 2 + ((self.a - self.b) / 2) ** 2)
        return self.a + self.b + 2 * side

    def __str__(self):
        return f"Trapezoid: a={self.a}, b={self.b}, h={self.h}, color={self.color}, area={self.area():.2f}"

    def draw(self, label="", save_path=None):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Vertices of isosceles trapezoid
        half_diff = abs(self.a - self.b) / 2
        if self.a > self.b:
            x = [-self.a / 2, self.a / 2, self.b / 2, -self.b / 2]
        else:
            x = [-self.a / 2, self.a / 2, self.b / 2, -self.b / 2]
        y = [-self.h / 2, -self.h / 2, self.h / 2, self.h / 2]

        poly = patches.Polygon(list(zip(x, y)), closed=True, facecolor=self.color, edgecolor='black', linewidth=2)
        ax.add_patch(poly)

        if label:
            ax.text(0, -self.h / 2 - 0.3, label, ha='center', fontsize=12)

        ax.set_xlim(-max(self.a, self.b) / 2 - 1, max(self.a, self.b) / 2 + 1)
        ax.set_ylim(-self.h / 2 - 1, self.h / 2 + 1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path)
        plt.show()


def run():
    print("\n=== TASK 4: ISOSCELES TRAPEZOID ===")

    try:
        a = float(input("Enter lower base (a): "))
        b = float(input("Enter upper base (b): "))
        h = float(input("Enter height (h): "))
        color = input("Enter color (blue/red/green): ") or "blue"
        label = input("Enter text label: ")

        if a <= 0 or b <= 0 or h <= 0:
            print("Error: All values must be positive")
            return

        trap = IsoscelesTrapezoid(a, b, h, color)
        print("\n" + str(trap))

        # Change color to demonstrate property
        print(f"\nChanging color to red...")
        trap.color = "red"
        print(f"New color: {trap.color}")

        draw_choice = input("\nDraw shape? (y/n): ")
        if draw_choice.lower() == 'y':
            trap.draw(label, "trapezoid.png")

    except ValueError:
        print("Invalid input")