print("PROGRAMMING PARADIGM LEARNING CURVES - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# 1. BASIC DATASET INFORMATION
print("\n1. BASIC DATASET INFORMATION")
print("-" * 40)

print(f"Dataset dimensions: {df_proper.shape[0]} rows × {df_proper.shape[1]} columns")
print(f"Total number of developers: {len(df_proper)}")
print(f"Number of variables: {len(df_proper.columns)}")

# List all columns with their data types
print("\nDataset columns and data types:")
for i, (col, dtype) in enumerate(df_proper.dtypes.items(), 1):
    print(f"{i:2d}. {col:30} : {dtype}")

# 2. DEMOGRAPHIC ANALYSIS
print("\n\n2. DEMOGRAPHIC ANALYSIS")
print("-" * 40)

# Age analysis
print("\nAge Statistics:")
print(f"  Mean age: {df_proper['Age'].mean():.1f} years")
print(f"  Median age: {df_proper['Age'].median():.1f} years")
print(f"  Age range: {df_proper['Age'].min()} to {df_proper['Age'].max()} years")
print(f"  Standard deviation: {df_proper['Age'].std():.1f} years")

# Age distribution
age_bins = [20, 25, 30, 35, 40, 45]
age_labels = ['20-24', '25-29', '30-34', '35-39', '40+']
df_proper['Age_Group'] = pd.cut(df_proper['Age'], bins=age_bins, labels=age_labels, right=False)

print("\nAge Group Distribution:")
age_dist = df_proper['Age_Group'].value_counts().sort_index()
for group, count in age_dist.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {group}: {count} developers ({percentage:.1f}%)")

# Gender distribution
print("\nGender Distribution:")
gender_counts = df_proper['Gender'].value_counts()
for gender, count in gender_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {gender}: {count} developers ({percentage:.1f}%)")

# Education level
print("\nEducation Level Distribution:")
education_counts = df_proper['Education_Level'].value_counts()
for edu, count in education_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {edu}: {count} developers ({percentage:.1f}%)")

# Country distribution (top 10)
print("\nTop 10 Countries by Developer Count:")
country_counts = df_proper['Country'].value_counts().head(10)
for country, count in country_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {country}: {count} developers ({percentage:.1f}%)")

# 3. PROFESSIONAL BACKGROUND ANALYSIS
print("\n\n3. PROFESSIONAL BACKGROUND ANALYSIS")
print("-" * 40)

# Years of programming experience
print("\nProgramming Experience (Years):")
print(f"  Mean experience: {df_proper['Years_Programming'].mean():.1f} years")
print(f"  Median experience: {df_proper['Years_Programming'].median():.1f} years")
print(f"  Range: {df_proper['Years_Programming'].min():.1f} to {df_proper['Years_Programming'].max():.1f} years")

# Experience categories
print("\nExperience Level Distribution:")
exp_counts = df_proper['Experience_Level'].value_counts()
for level, count in exp_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {level}: {count} developers ({percentage:.1f}%)")

# Employment status
print("\nEmployment Status Distribution:")
emp_counts = df_proper['Employment_Status'].value_counts()
for status, count in emp_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {status}: {count} developers ({percentage:.1f}%)")

# Primary roles
print("\nTop 10 Primary Roles:")
role_counts = df_proper['Primary_Role'].value_counts().head(10)
for role, count in role_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {role}: {count} developers ({percentage:.1f}%)")

# Company size
print("\nCompany Size Distribution:")
company_counts = df_proper['Company_Size'].value_counts()
for size, count in company_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {size}: {count} developers ({percentage:.1f}%)")

# 4. PROGRAMMING SKILLS ANALYSIS
print("\n\n4. PROGRAMMING SKILLS ANALYSIS")
print("-" * 40)

# Number of programming languages
print("\nNumber of Programming Languages Known:")
print(f"  Mean: {df_proper['Languages_Count'].mean():.1f} languages")
print(f"  Median: {df_proper['Languages_Count'].median():.1f} languages")
print(f"  Range: {df_proper['Languages_Count'].min()} to {df_proper['Languages_Count'].max()} languages")

# Paradigms experienced
print("\nNumber of Programming Paradigms Experienced:")
print(f"  Mean: {df_proper['Paradigms_Experienced'].mean():.1f} paradigms")
print(f"  Median: {df_proper['Paradigms_Experienced'].median():.1f} paradigms")
print(f"  Range: {df_proper['Paradigms_Experienced'].min()} to {df_proper['Paradigms_Experienced'].max()} paradigms")

# Primary paradigm preference
print("\nPrimary Paradigm Preference:")
paradigm_counts = df_proper['Primary_Paradigm'].value_counts()
for paradigm, count in paradigm_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {paradigm}: {count} developers ({percentage:.1f}%)")

# Projects completed
print("\nProjects Completed:")
print(f"  Mean: {df_proper['Projects_Completed'].mean():.1f} projects")
print(f"  Median: {df_proper['Projects_Completed'].median():.1f} projects")
print(f"  Range: {df_proper['Projects_Completed'].min()} to {df_proper['Projects_Completed'].max()} projects")

# Weekly programming hours
print("\nWeekly Programming Hours:")
print(f"  Mean: {df_proper['Hours_Per_Week'].mean():.1f} hours/week")
print(f"  Median: {df_proper['Hours_Per_Week'].median():.1f} hours/week")
print(f"  Range: {df_proper['Hours_Per_Week'].min()} to {df_proper['Hours_Per_Week'].max()} hours/week")

# Formal CS training
print("\nFormal Computer Science Training:")
formal_counts = df_proper['Formal_CS_Training'].value_counts()
for training, count in formal_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {training}: {count} developers ({percentage:.1f}%)")