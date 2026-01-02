print("\n=== FILLING MISSING VALUES WITH REASONABLE ESTIMATES ===")

# For the missing columns, let's use the median from the first 24 rows
missing_cols = ['Learning_Curve_Steepness', 'Knowledge_Retention', 
                'Difficulty_Transitioning', 'Mental_Model_Shift']

print("Calculating median values from first 24 rows:")
for col in missing_cols:
    median_val = df_proper[col].median()
    print(f"  {col}: {median_val:.2f}")
    
    # Fill missing values with median
    df_proper[col].fillna(median_val, inplace=True)

print("\n=== DATASET AFTER FILLING MISSING VALUES ===")
print(f"Shape: {df_proper.shape}")
print(f"Total missing values now: {df_proper.isnull().sum().sum()}")

# Let's verify by checking a sample of previously missing rows
print("\n=== VERIFICATION OF FILLED VALUES ===")
print("Sample rows (ID 25-30) with previously missing columns:")
sample_cols = ['ID', 'Learning_Curve_Steepness', 'Knowledge_Retention', 
               'Difficulty_Transitioning', 'Mental_Model_Shift']
print(df_proper[df_proper['ID'].between(25, 30)][sample_cols])

# Now let's create some derived features for analysis
print("\n=== CREATING DERIVED FEATURES FOR ANALYSIS ===")

# 1. Calculate average difficulty across all paradigms
difficulty_cols = ['Imperative_Difficulty', 'Functional_Difficulty',
                   'Object_Oriented_Difficulty', 'Logic_Difficulty',
                   'Reactive_Difficulty', 'Declarative_Difficulty']

df_proper['Avg_Difficulty'] = df_proper[difficulty_cols].mean(axis=1)

# 2. Calculate total learning time (sum of months for all paradigms)
months_cols = ['Imperative_Months', 'Functional_Months', 'Object_Oriented_Months',
               'Logic_Months', 'Reactive_Months', 'Declarative_Months']

df_proper['Total_Learning_Months'] = df_proper[months_cols].sum(axis=1)

# 3. Create experience categories
def categorize_experience(years):
    if years < 2:
        return 'Beginner (<2 years)'
    elif years < 5:
        return 'Intermediate (2-5 years)'
    elif years < 10:
        return 'Experienced (5-10 years)'
    else:
        return 'Expert (10+ years)'

df_proper['Experience_Level'] = df_proper['Years_Programming'].apply(categorize_experience)

# 4. Create salary categories (for analysis)
def categorize_salary(salary):
    if salary < 50000:
        return 'Low (<50k)'
    elif salary < 100000:
        return 'Medium (50k-100k)'
    elif salary < 150000:
        return 'High (100k-150k)'
    else:
        return 'Very High (150k+)'

df_proper['Salary_Category'] = df_proper['Current_Salary_USD'].apply(categorize_salary)

# 5. Calculate paradigm diversity score
df_proper['Paradigm_Diversity'] = df_proper['Paradigms_Experienced'] / 5  # Normalize to 0-1 scale

print("\n=== DERIVED FEATURES CREATED ===")
print("1. Avg_Difficulty: Average difficulty across all paradigms")
print("2. Total_Learning_Months: Total time to learn all paradigms")
print("3. Experience_Level: Categorized experience levels")
print("4. Salary_Category: Categorized salary levels")
print("5. Paradigm_Diversity: Normalized paradigm experience")

# Save the cleaned dataset for future use
print("\n=== SAVING CLEANED DATASET ===")
df_proper.to_csv('/kaggle/working/programming_paradigms_clean.csv', index=False)
print("Dataset saved as 'programming_paradigms_clean.csv' in working directory")

# Display final dataset information
print("\n=== FINAL DATASET OVERVIEW ===")
print(f"Total rows: {len(df_proper)}")
print(f"Total columns: {len(df_proper.columns)}")
print(f"Total derived features added: 5")

print("\n=== FINAL DATASET SAMPLE (with derived features) ===")
sample_cols_display = ['ID', 'Age', 'Years_Programming', 'Experience_Level', 
                       'Primary_Paradigm', 'Avg_Difficulty', 'Total_Learning_Months',
                       'Current_Salary_USD', 'Salary_Category', 'Paradigm_Diversity']
print(df_proper[sample_cols_display].head(10))