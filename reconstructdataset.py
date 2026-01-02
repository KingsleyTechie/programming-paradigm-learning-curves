print("\n=== RECONSTRUCTING THE COMPLETE DATASET ===")

# We have two different row structures:
# 1. First 25 rows (0-24): Complete with 38 columns
# 2. Remaining rows (25-153): Only 26 columns (missing last 12)

# Let's separate them properly
complete_rows = all_rows[:25]  # Rows 0-24 (25 rows, includes header)
partial_rows = all_rows[25:]   # Rows 25-153 (129 rows)

print(f"Complete rows: {len(complete_rows)} (including header)")
print(f"Partial rows: {len(partial_rows)}")
print(f"Expected columns: 38")

# Get the header from complete rows
header = complete_rows[0]
print(f"\nHeader columns: {len(header)}")

# Now let's reconstruct the partial rows
print("\n=== RECONSTRUCTING PARTIAL ROWS ===")

# Based on our analysis, partial rows have 26 columns, but should have 38
# This means they're missing the last 12 columns
# Looking at the data pattern, the missing columns are likely:
# 26. Reactive_Months
# 27. Declarative_Months
# 28. Learning_Curve_Steepness
# 29. Plateau_Experienced
# 30. Knowledge_Retention
# 31. Difficulty_Transitioning
# 32. Prefer_First_Paradigm
# 33. Mental_Model_Shift
# 34. Preferred_Learning_Method
# 35. Motivation_Factors
# 36. Biggest_Challenge
# 37. Transferable_Skills

# But wait, looking at line 25 again:
# It has values like "Peer programming", "Problem-solving fun", "Reactive streams", "Event handling"
# These should be in columns 34-37, but they appear at the end of the 26 columns

# Actually, I think the partial rows DO contain the qualitative data,
# but they're shifted. Let me check:

print("\nAnalyzing partial row structure:")
sample_partial_row = partial_rows[0]  # Row 25 in original data
print(f"Sample partial row (ID={sample_partial_row[0]}):")
for i, val in enumerate(sample_partial_row):
    print(f"  Col {i:2d}: {val}")

print(f"\nTotal values in partial row: {len(sample_partial_row)}")

# Looking at this, I think columns 0-25 are correct (matching the first 26 columns of complete rows)
# But we're missing numerical data for some columns

# Let me create a mapping based on comparing complete and partial rows
print("\n=== CREATING COMPLETE DATASET ===")

# First, create a DataFrame from complete rows (excluding header for data)
complete_data = []
for row in complete_rows[1:]:  # Skip header
    complete_data.append(row)

# Create a list to hold all reconstructed data
all_reconstructed_data = []

# Process complete rows (already have all 38 columns)
for row in complete_data:
    all_reconstructed_data.append(row)

# Process partial rows - need to reconstruct missing values
print(f"\nReconstructing {len(partial_rows)} partial rows...")

# Based on analysis, partial rows have columns 0-25
# We need to add placeholders for columns 26-37
for row in partial_rows:
    reconstructed_row = row.copy()  # Start with existing 26 columns
    
    # Add placeholder for missing columns 26-37
    # We'll use NaN for numeric columns and empty string for text columns
    for i in range(26, 38):
        # Determine column type based on header position
        col_name = header[i] if i < len(header) else f"Column_{i}"
        
        # Check if this should be numeric or text
        if any(word in col_name.lower() for word in ['months', 'difficulty', 'steepness', 
                                                     'retention', 'transitioning', 'shift', 'salary']):
            reconstructed_row.append(np.nan)  # Numeric placeholder
        else:
            reconstructed_row.append('')  # Text placeholder
    
    all_reconstructed_data.append(reconstructed_row)

print(f"Total reconstructed rows: {len(all_reconstructed_data)}")

# Create DataFrame
df_clean = pd.DataFrame(all_reconstructed_data, columns=header)

print(f"\nClean dataset shape: {df_clean.shape}")
print(f"Columns: {len(df_clean.columns)}")

# Convert data types
print("\nConverting data types...")

# Convert ID to int
df_clean['ID'] = pd.to_numeric(df_clean['ID'], errors='coerce')

# Convert numeric columns
numeric_columns = ['Age', 'Years_Programming', 'Languages_Count', 'Paradigms_Experienced',
                   'Projects_Completed', 'Hours_Per_Week', 'Current_Salary_USD',
                   'Imperative_Difficulty', 'Object_Oriented_Difficulty', 
                   'Logic_Difficulty', 'Declarative_Difficulty',
                   'Reactive_Months', 'Declarative_Months', 'Learning_Curve_Steepness',
                   'Knowledge_Retention', 'Difficulty_Transitioning', 'Mental_Model_Shift']

for col in numeric_columns:
    if col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Convert Functional_Difficulty and Reactive_Difficulty (they might have mixed types)
# First, let's see what values they contain
print("\n=== CHECKING PROBLEMATIC COLUMNS ===")
print("Functional_Difficulty unique values:")
print(df_clean['Functional_Difficulty'].unique()[:20])

print("\nReactive_Difficulty unique values:")
print(df_clean['Reactive_Difficulty'].unique()[:20])

# Clean these columns - extract numeric values where possible
def extract_numeric(value):
    if pd.isna(value):
        return np.nan
    try:
        # Try direct conversion
        return float(value)
    except:
        # Check if it's a string that contains a number
        if isinstance(value, str):
            # Remove non-numeric characters except decimal point
            cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
            if cleaned:
                try:
                    return float(cleaned)
                except:
                    return np.nan
        return np.nan

# Apply cleaning
df_clean['Functional_Difficulty'] = df_clean['Functional_Difficulty'].apply(extract_numeric)
df_clean['Reactive_Difficulty'] = df_clean['Reactive_Difficulty'].apply(extract_numeric)

# Convert month columns
month_columns = ['Imperative_Months', 'Functional_Months', 'Object_Oriented_Months', 'Logic_Months']
for col in month_columns:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# Display sample
print("\n=== CLEAN DATASET SAMPLE ===")
print(df_clean.head(10))

print("\n=== DATASET INFO ===")
print(df_clean.info())

print("\n=== MISSING VALUES SUMMARY ===")
missing_summary = df_clean.isnull().sum()
print(missing_summary[missing_summary > 0])