print("\n=== CHECKING DATA SHIFT PATTERN ===")

# Check rows 20-30 to see exactly where the shift happens
print("\nRows 20-25 (where shift likely begins):")
for i in range(20, 26):
    print(f"\nRow {i}:")
    print(f"  Functional_Difficulty: {df.loc[i, 'Functional_Difficulty']}")
    print(f"  Imperative_Months: {df.loc[i, 'Imperative_Months']}")

# Let's also check the structure of the first few good rows
print("\n\n=== FIRST FEW CORRECT ROWS ===")
print("Row 0 (correct structure):")
print(f"  Functional_Difficulty: {df.loc[0, 'Functional_Difficulty']} (should be numeric)")
print(f"  Imperative_Months: {df.loc[0, 'Imperative_Months']} (should be numeric)")
print(f"  Plateau_Experienced: {df.loc[0, 'Plateau_Experienced']} (should be Yes/No)")

print("\nRow 23 (last correct row?):")
print(f"  Functional_Difficulty: {df.loc[23, 'Functional_Difficulty']}")
print(f"  Imperative_Months: {df.loc[23, 'Imperative_Months']}")
print(f"  Plateau_Experienced: {df.loc[23, 'Plateau_Experienced']}")