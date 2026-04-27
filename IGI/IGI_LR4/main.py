"""
Lab Works 1-6
Author: Borsuk Daniil Vadimovich
Version: 1.0.0
Date: 2026-04-27
"""

import task1
import task2
import task3
import task4
import task5
import task6


def main():
    print("=" * 50)
    print("LABORATORY WORKS 1-6")
    print("Author: Borsuk Daniil Vadimovich")
    print("=" * 50)

    while True:
        print("\nMENU:")
        print("1 - Library Catalog (Task 1)")
        print("2 - Text Analysis (Task 2)")
        print("3 - Series ln(1+x) with tabulate (Task 3)")
        print("4 - Isosceles Trapezoid (Task 4)")
        print("5 - NumPy Matrix Analysis (Task 5)")
        print("6 - Pandas Boston Housing (Task 6)")
        print("0 - Exit")

        choice = input("\nYour choice: ")

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            task1.run()
        elif choice == "2":
            task2.run()
        elif choice == "3":
            task3.run()
            task3.stats_demo()  # Additional statistics demo
        elif choice == "4":
            task4.run()
        elif choice == "5":
            task5.run()
        elif choice == "6":
            task6.run()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()