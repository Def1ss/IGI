"""
Task 6: Boston Housing analysis with Pandas using train.csv
"""

import pandas as pd


def run():
    print("\n=== TASK 6: BOSTON HOUSING ANALYSIS ===")

    # Load data from file
    try:
        df = pd.read_csv("train.csv")
        print("Loaded train.csv")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
    except FileNotFoundError:
        print("Error: train.csv not found")
        return

    # Create crime_stats DataFrame from dictionary using real data from file
    # Take first 10 districts from the dataset
    n_districts = min(10, len(df))
    crime_stats = pd.DataFrame({
        'district': [f'District_{i}' for i in range(1, n_districts + 1)],
        'crime_rate': df['crim'].head(n_districts).tolist(),
        'avg_rooms': df['rm'].head(n_districts).tolist()
    })
    print("\nCrime Statistics DataFrame (using real crim and rm data):")
    print(crime_stats.to_string(index=False))

    # Access with .loc and .iloc
    print("\nFirst row using .loc[0]:")
    print(crime_stats.loc[0])
    print("\nFirst row using .iloc[0]:")
    print(crime_stats.iloc[0])

    # Main analysis: compare MEDV for high vs low NOX
    df_sorted = df.sort_values('nox')
    n = len(df)
    n_high = n_low = max(1, int(n * 0.3))

    high_nox = df_sorted.tail(n_high)
    low_nox = df_sorted.head(n_low)

    avg_medv_high = high_nox['medv'].mean()
    avg_medv_low = low_nox['medv'].mean()
    ratio = avg_medv_high / avg_medv_low

    print("\n" + "="*50)
    print("MAIN RESULT")
    print("="*50)
    print(f"Districts with highest NOX (top 30%): {n_high} districts")
    print(f"Average MEDV (high NOX): ${avg_medv_high:.2f}K")
    print(f"Districts with lowest NOX (bottom 30%): {n_low} districts")
    print(f"Average MEDV (low NOX): ${avg_medv_low:.2f}K")
    print(f"\nRatio (high NOX / low NOX): {ratio:.2f}")
    print("="*50)

    # Additional statistics
    print("\nDescriptive statistics for MEDV:")
    print(df['medv'].describe())

    print("\nCorrelation matrix (selected columns):")
    corr_matrix = df[['medv', 'nox', 'rm', 'crim', 'lstat']].corr()
    print(corr_matrix)

    print("\nCorrelation with MEDV:")
    print(corr_matrix['medv'].sort_values(ascending=False))

    # Statistical methods demonstration
    print("\n" + "="*50)
    print("STATISTICAL ANALYSIS")
    print("="*50)
    print(f"Mean MEDV: {df['medv'].mean():.2f}")
    print(f"Median MEDV: {df['medv'].median():.2f}")
    print(f"Variance MEDV: {df['medv'].var():.2f}")
    print(f"Std Deviation MEDV: {df['medv'].std():.2f}")
    print(f"Min MEDV: {df['medv'].min():.2f}")
    print(f"Max MEDV: {df['medv'].max():.2f}")


    # Save results
    df.to_csv("boston_analysis_output.csv", index=False)
    print("\nSaved dataset to boston_analysis_output.csv")