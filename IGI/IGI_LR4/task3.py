"""
Task 3: Maclaurin series for ln(1+x) with plotting and tabulate
"""

import math
import matplotlib.pyplot as plt
from tabulate import tabulate


def ln_series(x, eps=1e-6, max_n=500):
    """Calculate ln(1+x) using series"""
    total = 0
    for n in range(1, max_n + 1):
        term = ((-1) ** (n - 1)) * (x ** n) / n
        total += term
        if abs(term) < eps:
            return n, total
    return max_n, total


def run():
    print("\n=== TASK 3: ln(1+x) SERIES ===")
    print("Series: ln(1+x) = x - x^2/2 + x^3/3 - ...")

    try:
        x = float(input("Enter x (|x| < 1): "))
        if abs(x) >= 1:
            print("Error: |x| must be < 1")
            return

        eps = float(input("Enter precision (e.g., 0.001): "))

        n, series_val = ln_series(x, eps)
        math_val = math.log(1 + x)

        print(f"\nTerms used: {n}")
        print(f"Series result: {series_val:.8f}")
        print(f"math.log result: {math_val:.8f}")
        print(f"Error: {abs(series_val - math_val):.2e}")

        # Generate table using tabulate
        print("\nTable of values:")
        table_data = []
        for xv in [-0.5, -0.25, 0, 0.25, 0.5, 0.75]:
            try:
                nv, sv = ln_series(xv, 1e-5, 15)
                mv = math.log(1 + xv)
                table_data.append([xv, nv, sv, mv, abs(sv-mv)])
            except:
                table_data.append([xv, "-", "-", "-", "-"])

        headers = ["x", "n", "F(x)", "Math F(x)", "Error"]
        print(tabulate(table_data, headers=headers, floatfmt=(".2f", "d", ".6f", ".6f", ".2e"), tablefmt="grid"))

        # Plot
        plot_choice = input("\nGenerate plot? (y/n): ")
        if plot_choice.lower() == 'y':
            x_vals = [i / 100 for i in range(-99, 100, 10)]
            series_vals = []
            math_vals = []
            for xv in x_vals:
                if abs(xv) < 1:
                    _, sv = ln_series(xv, 1e-6, 30)
                    series_vals.append(sv)
                    math_vals.append(math.log(1 + xv))

            plt.figure(figsize=(10, 5))
            plt.plot(x_vals, series_vals, 'b-', label='Series', linewidth=2)                                                     # color = blue , linestyle = "solid"
            plt.plot(x_vals, math_vals, 'r--', label='math.log', linewidth=2)                                                    # color = red , linestyle = "dashed"
            plt.xlabel('x')
            plt.ylabel('ln(1+x)')
            plt.title('Maclaurin Series for ln(1+x)')
            plt.legend()
            plt.grid(True)
            plt.savefig("series_plot.png")
            plt.show()
            print("Plot saved to series_plot.png")

    except ValueError:
        print("Invalid input")


def stats_demo():
    """Simple statistics functions"""
    data = [1, 2, 2, 3, 4, 5, 5, 5, 6]
    mean = sum(data) / len(data)
    median = sorted(data)[len(data) // 2]
    mode = max(set(data), key=data.count)
    var = sum((x - mean) ** 2 for x in data) / len(data)

    print("\nStatistics demo:")
    print(f"Data: {data}")
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Variance: {var:.2f}")
    print(f"Std Dev: {math.sqrt(var):.2f}")