# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
%matplotlib inline

# Load the dataset with the correct path
print("Loading dataset...")
df = pd.read_csv('/kaggle/input/learningcurves-csv/learningcurves.csv')

# Initial exploration
print("\n=== DATASET OVERVIEW ===")
print(f"Dataset shape: {df.shape}")
print(f"Number of records: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

print("\n=== COLUMN NAMES ===")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== FIRST 5 ROWS ===")
pd.set_option('display.max_columns', None)  # Show all columns
print(df.head())

print("\n=== BASIC STATISTICS (Numerical Columns) ===")
print(df.describe())

print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
print(missing[missing > 0])
if missing.sum() == 0:
    print("No missing values found!")