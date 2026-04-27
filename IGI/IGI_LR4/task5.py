"""
Task 5: NumPy matrix analysis
"""

import numpy as np


def run():
    print("\n=== TASK 5: NUMPY MATRIX ANALYSIS ===")

    try:
        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))

        # Create random matrix
        matrix = np.random.randint(0, 100, size=(rows, cols))

        print("\nMatrix:")
        print(matrix)

        # Statistics
        print(f"\nMean: {np.mean(matrix):.2f}")
        print(f"Median: {np.median(matrix):.2f}")
        print(f"Variance: {np.var(matrix):.2f}")
        print(f"Std Dev: {np.std(matrix):.2f}")

        # Row sums
        row_sums = np.sum(matrix, axis=1)
        print(f"\nRow sums: {row_sums}")
        min_sum = np.min(row_sums)
        min_idx = np.argmin(row_sums)
        print(f"Minimum row sum: {min_sum} (row {min_idx})")

        # Split by parity of i+j
        even_elems = []
        odd_elems = []
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    even_elems.append(matrix[i, j])
                else:
                    odd_elems.append(matrix[i, j])

        even_arr = np.array(even_elems)
        odd_arr = np.array(odd_elems)

        print(f"\nElements with even i+j: {len(even_arr)}")
        print(f"Elements with odd i+j: {len(odd_arr)}")

        # Correlation coefficient
        if len(even_arr) == len(odd_arr) and len(even_arr) > 1:
            corr = np.corrcoef(even_arr, odd_arr)[0, 1]
            print(f"Correlation coefficient: {corr:.6f}")
        else:
            # Truncate to same length
            min_len = min(len(even_arr), len(odd_arr))
            if min_len > 1:
                corr = np.corrcoef(even_arr[:min_len], odd_arr[:min_len])[0, 1]
                print(f"Correlation coefficient: {corr:.6f}")
            else:
                print("Not enough data for correlation")

        # Additional operations
        print(f"\nMatrix shape: {matrix.shape}")
        print(f"First row: {matrix[0, :]}")
        if rows > 1 and cols > 1:
            print(f"First 2x2 submatrix:\n{matrix[0:2, 0:2]}")
        print(f"Square root of first element: {np.sqrt(matrix[0, 0]):.2f}")

    except ValueError:
        print("Invalid input")