print("\n=== ANALYZING THE DATA MAPPING ISSUE ===")

# Look at row 24 (index 24 in df_clean, which corresponds to ID 25)
print("Row with ID 25 (index 24 in df_clean):")
row_24 = df_clean[df_clean['ID'] == 25].iloc[0]
print(f"  Functional_Difficulty: {row_24['Functional_Difficulty']} (should be numeric, but is NaN)")
print(f"  Plateau_Experienced: {row_24['Plateau_Experienced']} (should be Yes/No, but has 'No')")
print(f"  Preferred_Learning_Method: {row_24['Preferred_Learning_Method']} (has 'Project-based')")

# The pattern is clear: In rows 24-153:
# - Columns 29-37 (qualitative data) actually contain data for columns 17-28
# - Columns 17-28 are empty/missing

# Let me check what's really in the qualitative columns for these rows
print("\n=== CHECKING ACTUAL DATA IN QUALITATIVE COLUMNS FOR ROWS 24-153 ===")

# For rows 24-153, check what's in the qualitative columns
sample_row = df_clean.iloc[24]  # ID 25
print(f"\nSample row (ID={sample_row['ID']}):")
print(f"  Plateau_Experienced: {sample_row['Plateau_Experienced']}")
print(f"  Prefer_First_Paradigm: {sample_row['Prefer_First_Paradigm']}")
print(f"  Preferred_Learning_Method: {sample_row['Preferred_Learning_Method']}")
print(f"  Motivation_Factors: {sample_row['Motivation_Factors']}")
print(f"  Biggest_Challenge: {sample_row['Biggest_Challenge']}")
print(f"  Transferable_Skills: {sample_row['Transferable_Skills']}")

# Now I understand! In rows 24-153:
# The values in qualitative columns (29-37) are actually:
# - 'No' in Plateau_Experienced → should be in Functional_Difficulty?
# - 'Project-based' in Preferred_Learning_Method → should be in Imperative_Months?
# But wait, that doesn't make sense...

# Let me look at the raw data again for row 25 (ID 25)
print("\n=== EXAMINING RAW DATA PATTERN ===")
print("Raw CSV line 25 (ID 25):")
print(all_rows[25])

# Based on the raw data: [25, 31, 'Non-binary', "Master's Degree", 'USA', 'Full-time', '8', 
# 'Full Stack Developer', 'Large (1000+)', '6', '4', 'Object-Oriented', '19', '46', 'Yes', 
# '86000', '3', 'No', '3', '2', 'Yes', '2', 'Project-based', 'Career advancement', 
# 'Design patterns', 'Software design']

# I think the real issue is different. Looking at the pattern:
# - 'No' at position 17 → This is actually Plateau_Experienced value
# - 'Yes' at position 20 → This is actually Prefer_First_Paradigm value
# - 'Project-based' at position 22 → This is actually Preferred_Learning_Method
# - 'Career advancement' at position 23 → This is actually Motivation_Factors
# - 'Design patterns' at position 24 → This is actually Biggest_Challenge
# - 'Software design' at position 25 → This is actually Transferable_Skills

# So the issue is: In rows 24-153, columns 17-25 contain data for columns 29-37!
# And columns 26-37 are completely missing.

print("\n=== IMPLEMENTING THE CORRECT FIX ===")

# Create a copy of the clean dataframe to fix
df_final = df_clean.copy()

# For rows 24-153 (ID 25-153), we need to:
# 1. Move data from columns 17-25 to columns 29-37
# 2. Set columns 17-28 to appropriate values (we'll need to fill these)

# First, let's identify the rows that need fixing (ID >= 25)
mask = df_final['ID'] >= 25

print(f"Rows to fix: {mask.sum()}")

# Create a mapping of where data should go
# Based on analysis of row ID 25:
# Col 17 ('No') → Should go to Plateau_Experienced (col 29)
# Col 20 ('Yes') → Should go to Prefer_First_Paradigm (col 32)
# Col 22 ('Project-based') → Should go to Preferred_Learning_Method (col 34)
# Col 23 ('Career advancement') → Should go to Motivation_Factors (col 35)
# Col 24 ('Design patterns') → Should go to Biggest_Challenge (col 36)
# Col 25 ('Software design') → Should go to Transferable_Skills (col 37)

# But wait, we also have columns 18, 19, 21 which contain numeric values
# These might actually be correct for Object_Oriented_Difficulty, Logic_Difficulty, Declarative_Difficulty

print("\n=== CREATING PROPER MAPPING ===")

# Let me create a function to properly map the data
def fix_row(row):
    """Fix a single row's data mapping"""
    if row['ID'] < 25:
        return row  # Rows 1-24 are already correct
    
    # Create a copy of the row
    fixed_row = row.copy()
    
    # Based on the pattern in ID 25:
    # The row has data in positions that correspond to:
    # Current Functional_Difficulty (col 17) → Actually Plateau_Experienced
    # Current Object_Oriented_Difficulty (col 18) → Might be correct? It's '3' which looks like a difficulty rating
    # Current Logic_Difficulty (col 19) → Might be correct? It's '2' which looks like a difficulty rating
    # Current Reactive_Difficulty (col 20) → Actually Prefer_First_Paradigm
    # Current Declarative_Difficulty (col 21) → Might be correct? It's '2' which looks like a difficulty rating
    # Current Imperative_Months (col 22) → Actually Preferred_Learning_Method
    # Current Functional_Months (col 23) → Actually Motivation_Factors
    # Current Object_Oriented_Months (col 24) → Actually Biggest_Challenge
    # Current Logic_Months (col 25) → Actually Transferable_Skills
    
    # Extract values
    val_17 = row['Functional_Difficulty']  # Actually Plateau_Experienced
    val_18 = row['Object_Oriented_Difficulty']  # Might be correct
    val_19 = row['Logic_Difficulty']  # Might be correct
    val_20 = row['Reactive_Difficulty']  # Actually Prefer_First_Paradigm
    val_21 = row['Declarative_Difficulty']  # Might be correct
    val_22 = row['Imperative_Months']  # Actually Preferred_Learning_Method
    val_23 = row['Functional_Months']  # Actually Motivation_Factors
    val_24 = row['Object_Oriented_Months']  # Actually Biggest_Challenge
    val_25 = row['Logic_Months']  # Actually Transferable_Skills
    
    # Map values to correct columns
    # For boolean-like values in col 17 and 20
    if pd.notna(val_17):
        if str(val_17).lower() in ['yes', 'no']:
            fixed_row['Plateau_Experienced'] = str(val_17).capitalize()
            fixed_row['Functional_Difficulty'] = np.nan
        elif str(val_17).replace('.', '').isdigit():
            # It might actually be a numeric difficulty rating
            fixed_row['Functional_Difficulty'] = float(val_17)
    
    if pd.notna(val_20):
        if str(val_20).lower() in ['yes', 'no']:
            fixed_row['Prefer_First_Paradigm'] = str(val_20).capitalize()
            fixed_row['Reactive_Difficulty'] = np.nan
    
    # For text values that are clearly qualitative
    if pd.notna(val_22):
        val_str = str(val_22)
        # Check if it's a learning method
        learning_methods = ['project-based', 'mentorship', 'online courses', 'academic study',
                           'documentation', 'peer programming', 'tutorials', 'research papers', 'bootcamp']
        if any(method in val_str.lower() for method in learning_methods):
            fixed_row['Preferred_Learning_Method'] = val_str
            fixed_row['Imperative_Months'] = np.nan
    
    if pd.notna(val_23):
        val_str = str(val_23)
        # Check if it's a motivation factor
        motivation_terms = ['career', 'advancement', 'growth', 'problem', 'solving',
                           'intellectual', 'challenge', 'technical', 'elegance', 'job',
                           'requirements', 'practical', 'community', 'project', 'needs',
                           'theoretical', 'interest', 'employment', 'immediate']
        if any(term in val_str.lower() for term in motivation_terms):
            fixed_row['Motivation_Factors'] = val_str
            fixed_row['Functional_Months'] = np.nan
    
    if pd.notna(val_24):
        val_str = str(val_24)
        # Check if it's a challenge
        challenge_terms = ['abstract', 'thinking', 'pattern', 'recognition', 'state',
                          'management', 'mathematical', 'syntax', 'memorization',
                          'object', 'design', 'pure', 'functions', 'rule', 'based',
                          'type', 'systems', 'library', 'ecosystems']
        if any(term in val_str.lower() for term in challenge_terms):
            fixed_row['Biggest_Challenge'] = val_str
            fixed_row['Object_Oriented_Months'] = np.nan
    
    if pd.notna(val_25):
        val_str = str(val_25)
        # Check if it's a transferable skill
        skill_terms = ['algorithm', 'design', 'problem', 'decomposition', 'debugging',
                      'skills', 'architecture', 'patterns', 'basic', 'logic',
                      'code', 'organization', 'data', 'flow', 'sequential',
                      'abstraction', 'modular', 'design']
        if any(term in val_str.lower() for term in skill_terms):
            fixed_row['Transferable_Skills'] = val_str
            fixed_row['Logic_Months'] = np.nan
    
    return fixed_row

# Apply the fix
print("Applying fixes to rows 24-153...")
df_fixed = df_final.apply(fix_row, axis=1)

print("\n=== CHECKING FIXED DATA ===")
print("Sample fixed row (ID=25):")
sample_fixed = df_fixed[df_fixed['ID'] == 25].iloc[0]
print(f"  Plateau_Experienced: {sample_fixed['Plateau_Experienced']}")
print(f"  Prefer_First_Paradigm: {sample_fixed['Prefer_First_Paradigm']}")
print(f"  Preferred_Learning_Method: {sample_fixed['Preferred_Learning_Method']}")
print(f"  Motivation_Factors: {sample_fixed['Motivation_Factors']}")
print(f"  Biggest_Challenge: {sample_fixed['Biggest_Challenge']}")
print(f"  Transferable_Skills: {sample_fixed['Transferable_Skills']}")

print("\n=== CHECKING NUMERIC COLUMNS ===")
print(f"Functional_Difficulty non-null: {df_fixed['Functional_Difficulty'].notna().sum()}")
print(f"Reactive_Difficulty non-null: {df_fixed['Reactive_Difficulty'].notna().sum()}")

# Let's also check if we have reasonable values
print("\n=== SUMMARY OF FIXED DATASET ===")
print(f"Shape: {df_fixed.shape}")
print(f"Total rows: {len(df_fixed)}")

# Check missing values
print("\nMissing values after fix:")
missing_after = df_fixed.isnull().sum()
print(missing_after[missing_after > 0])