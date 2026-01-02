print("\n=== DATA QUALITY ASSESSMENT ===")

# Check the actual data for the problematic columns
print("\nChecking problematic columns sample:")
problem_columns = ['Functional_Difficulty', 'Reactive_Difficulty', 'Imperative_Months', 
                   'Functional_Months', 'Object_Oriented_Months', 'Logic_Months']
for col in problem_columns:
    print(f"\n{col} unique values (first 10):")
    print(df[col].unique()[:10])

# Let's see how the data looks at row 25-30 where issues might start
print("\n\n=== SAMPLE OF ROWS AROUND WHERE DATA MIGHT BE TRUNCATED ===")
print(df.iloc[24:32])

# Check if there's a pattern to the missing data
print("\n=== CHECKING FOR DATA TRUNCATION PATTERN ===")
# Let's look at row 24 (index 24) which seems to be where issues start
print("\nRow 24 (index 24):")
print(df.iloc[24])