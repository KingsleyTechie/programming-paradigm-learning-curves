print("\n=== ANALYZING COLUMN STRUCTURE FOR FIX ===")

# Let's examine what columns we have and their expected types
print("Expected column order (based on good rows 0-23):")
print("1. ID")
print("2. Age")
print("3. Gender")
print("...")
print("16. Current_Salary_USD")
print("17. Imperative_Difficulty")
print("18. Functional_Difficulty")
print("19. Object_Oriented_Difficulty")
print("20. Logic_Difficulty")
print("21. Reactive_Difficulty")
print("22. Declarative_Difficulty")
print("23. Imperative_Months")
print("24. Functional_Months")
print("25. Object_Oriented_Months")
print("26. Logic_Months")
print("27. Reactive_Months")
print("28. Declarative_Months")
print("29. Learning_Curve_Steepness")
print("30. Plateau_Experienced")
print("31. Knowledge_Retention")
print("32. Difficulty_Transitioning")
print("33. Prefer_First_Paradigm")
print("34. Mental_Model_Shift")
print("35. Preferred_Learning_Method")
print("36. Motivation_Factors")
print("37. Biggest_Challenge")
print("38. Transferable_Skills")

print("\n=== CHECKING WHERE THE SHIFT HAPPENS ===")
print("In bad rows (24+), 'Project-based' appears in Imperative_Months")
print("This suggests columns 29-38 have shifted to columns 23-32")

# Let's create a function to fix the data
print("\n=== CREATING CLEAN DATASET ===")

# First, let's separate good and bad rows
good_rows = df.iloc[:24].copy()  # Rows 0-23 are good
bad_rows = df.iloc[24:].copy()   # Rows 24+ need fixing

print(f"Good rows: {len(good_rows)}")
print(f"Bad rows to fix: {len(bad_rows)}")

# Let's see what the bad rows look like with correct column alignment
print("\n=== EXAMPLE OF BAD ROW BEFORE FIXING ===")
print("Row 24 (current bad state):")
print(f"  Current Imperative_Months: {bad_rows.iloc[0]['Imperative_Months']}")
print(f"  Current Functional_Months: {bad_rows.iloc[0]['Functional_Months']}")

# Based on the pattern, it looks like columns from 23 onward need to shift right
# Let's manually map where each value should go
print("\n\n=== MANUAL MAPPING ANALYSIS ===")
print("For row 24:")
print("  'No' in Functional_Difficulty should be in Plateau_Experienced?")
print("  'Project-based' in Imperative_Months should be in Preferred_Learning_Method?")
print("  'Career advancement' in Functional_Months should be in Motivation_Factors?")

# Let me create a test fix for one row to verify the pattern
test_row = bad_rows.iloc[0].copy()
print("\nTest row column mapping:")
print(f"1. Current Functional_Difficulty ('No') → Should be Plateau_Experienced?")
print(f"2. Current Imperative_Months ('Project-based') → Should be Preferred_Learning_Method?")
print(f"3. Current Functional_Months ('Career advancement') → Should be Motivation_Factors?")
print(f"4. Current Object_Oriented_Months ('Design patterns') → Should be Biggest_Challenge?")
print(f"5. Current Logic_Months ('Software design') → Should be Transferable_Skills?")

# Now let's implement the fix systematically
print("\n=== IMPLEMENTING DATA FIX ===")

# Create a copy of bad rows to fix
bad_rows_fixed = bad_rows.copy()

# Define the column shift mapping
# Columns 17-22 (difficulties) seem correct
# Columns 23-32 need to shift 6 positions to the right
# Columns 29-38 are missing (appear as NaN)

# Let me check the actual column indices
columns = list(df.columns)
print(f"\nTotal columns: {len(columns)}")
for i, col in enumerate(columns):
    print(f"{i}: {col}")