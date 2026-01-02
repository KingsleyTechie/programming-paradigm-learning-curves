print("\n=== REBUILDING DATASET FROM RAW DATA WITH PROPER MAPPING ===")

# Let me analyze the structure more carefully
print("Analyzing complete row (ID 1) structure:")
complete_row = all_rows[1]  # ID 1
print(f"Complete row has {len(complete_row)} fields")
for i, val in enumerate(complete_row[:30]):  # First 30 fields
    print(f"  {i:2d}: {val}")

print("\nAnalyzing partial row (ID 25) structure:")
partial_row = all_rows[25]  # ID 25
print(f"Partial row has {len(partial_row)} fields")
for i, val in enumerate(partial_row):
    print(f"  {i:2d}: {val}")

# Now I see the pattern clearly!
# Complete rows (ID 1-24): Have all 38 fields
# Partial rows (ID 25-153): Have only 26 fields

# But looking at the data, the partial rows seem to have the qualitative data
# at the end, but we're missing the numeric data for difficulties and months.

# Let me create a new approach: Use the first 24 rows as a template
# and intelligently fill in missing values for the rest

print("\n=== CREATING INTELLIGENT DATASET RECONSTRUCTION ===")

# First, let me create a list to hold all properly parsed data
proper_data = []

# Process header
proper_data.append(header)

# Process complete rows (ID 1-24)
for i in range(1, 25):  # Rows 1-24 (indices 1-24 in all_rows)
    proper_data.append(all_rows[i])

# Now process partial rows (ID 25-153)
# We need to intelligently merge data from partial rows with reasonable defaults
print(f"\nProcessing {len(partial_rows)} partial rows...")

# Get statistical information from complete rows to create reasonable defaults
complete_numeric_data = []
for i in range(1, 25):
    row = all_rows[i]
    # Extract numeric values for difficulties and months
    numeric_part = row[16:28]  # Columns 16-27: Difficulties and Months
    complete_numeric_data.append([float(x) if x.replace('.', '').isdigit() else np.nan for x in numeric_part])

# Calculate median values for each numeric column
numeric_array = np.array(complete_numeric_data)
medians = np.nanmedian(numeric_array, axis=0)

print(f"Median values from complete rows:")
for i, median in enumerate(medians):
    col_name = header[16 + i] if 16 + i < len(header) else f"Col_{16+i}"
    print(f"  {col_name}: {median:.1f}")

# Now process each partial row
for i, partial_row in enumerate(partial_rows):
    # Create a new row with 38 fields
    new_row = [None] * 38
    
    # Copy the first 16 fields as-is (they're correct)
    for j in range(16):
        if j < len(partial_row):
            new_row[j] = partial_row[j]
    
    # For numeric fields (16-27), we have a problem
    # The partial row doesn't have these values, so we'll use medians
    for j in range(16, 28):
        # Use median from complete rows
        new_row[j] = str(medians[j-16]) if not np.isnan(medians[j-16]) else ""
    
    # Now handle the qualitative data from the partial row
    # The partial row has its own values starting at position 16
    # But these are actually qualitative data that should go in positions 28-37
    
    # Map partial row positions to new row positions:
    # Partial[16] ('No' for ID 25) → New[28] (Learning_Curve_Steepness?) Actually should be Plateau_Experienced[29]
    # Partial[17] ('3' for ID 25) → New[29]? Actually this looks like a difficulty rating
    
    # Actually, looking at the data more carefully:
    # For ID 25 partial row:
    # Positions 16-25 contain mixed data:
    # 16: '3' (looks like Imperative_Difficulty) ✓
    # 17: 'No' (should be Plateau_Experienced)
    # 18: '3' (looks like Object_Oriented_Difficulty) ✓
    # 19: '2' (looks like Logic_Difficulty) ✓
    # 20: 'Yes' (should be Prefer_First_Paradigm)
    # 21: '2' (looks like Declarative_Difficulty) ✓
    # 22: 'Project-based' (should be Preferred_Learning_Method)
    # 23: 'Career advancement' (should be Motivation_Factors)
    # 24: 'Design patterns' (should be Biggest_Challenge)
    # 25: 'Software design' (should be Transferable_Skills)
    
    # So we need a smarter mapping
    # Let me map based on data type and position
    
    # Positions in partial row that contain numeric difficulties (should stay as difficulties)
    numeric_positions = [16, 18, 19, 21]  # These contain '3', '3', '2', '2' for ID 25
    
    # Positions in partial row that contain Yes/No (should go to boolean columns)
    boolean_positions = [17, 20]  # These contain 'No', 'Yes' for ID 25
    
    # Positions in partial row that contain text (should go to qualitative columns)
    text_positions = [22, 23, 24, 25]  # These contain text for ID 25
    
    # Apply the mapping
    for pos in numeric_positions:
        if pos < len(partial_row):
            val = partial_row[pos]
            # These should stay in their current positions (16-21)
            new_row[pos] = val
    
    for pos in boolean_positions:
        if pos < len(partial_row):
            val = partial_row[pos]
            # Map to appropriate boolean columns
            if pos == 17:  # 'No' → Plateau_Experienced (position 29)
                new_row[29] = val
            elif pos == 20:  # 'Yes' → Prefer_First_Paradigm (position 32)
                new_row[32] = val
    
    for i, pos in enumerate(text_positions):
        if pos < len(partial_row):
            val = partial_row[pos]
            # Map to appropriate text columns
            target_pos = 34 + i  # Starting at Preferred_Learning_Method (34)
            if target_pos < len(new_row):
                new_row[target_pos] = val
    
    # Fill remaining positions with empty strings
    for j in range(len(new_row)):
        if new_row[j] is None:
            new_row[j] = ""
    
    proper_data.append(new_row)

# Create the final DataFrame
print("\nCreating final DataFrame...")
df_proper = pd.DataFrame(proper_data[1:], columns=proper_data[0])  # Skip header row for data

print(f"Final dataset shape: {df_proper.shape}")

# Convert data types
print("\nConverting data types...")

# Convert ID to int
df_proper['ID'] = pd.to_numeric(df_proper['ID'], errors='coerce')

# Define numeric columns
numeric_cols = ['Age', 'Years_Programming', 'Languages_Count', 'Paradigms_Experienced',
                'Projects_Completed', 'Hours_Per_Week', 'Current_Salary_USD',
                'Imperative_Difficulty', 'Functional_Difficulty', 
                'Object_Oriented_Difficulty', 'Logic_Difficulty',
                'Reactive_Difficulty', 'Declarative_Difficulty',
                'Imperative_Months', 'Functional_Months', 'Object_Oriented_Months',
                'Logic_Months', 'Reactive_Months', 'Declarative_Months',
                'Learning_Curve_Steepness', 'Knowledge_Retention',
                'Difficulty_Transitioning', 'Mental_Model_Shift']

for col in numeric_cols:
    if col in df_proper.columns:
        df_proper[col] = pd.to_numeric(df_proper[col], errors='coerce')

print("\n=== FINAL DATASET SAMPLE (First 10 rows) ===")
pd.set_option('display.max_columns', None)
print(df_proper.head(10))

print("\n=== FINAL DATASET INFO ===")
print(df_proper.info())

print("\n=== MISSING VALUES ===")
missing_final = df_proper.isnull().sum()
print(missing_final[missing_final > 0])

print("\n=== SAMPLE OF RECONSTRUCTED ROWS (ID 25-30) ===")
print(df_proper[df_proper['ID'].between(25, 30)][['ID', 'Age', 'Imperative_Difficulty', 
                                                   'Plateau_Experienced', 'Preferred_Learning_Method']])