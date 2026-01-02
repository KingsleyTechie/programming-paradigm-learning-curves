# 5. SALARY AND COMPENSATION ANALYSIS
print("\n\n5. SALARY AND COMPENSATION ANALYSIS")
print("-" * 40)

# Current salary statistics
print("\nCurrent Salary Statistics (USD):")
print(f"  Mean salary: ${df_proper['Current_Salary_USD'].mean():,.0f}")
print(f"  Median salary: ${df_proper['Current_Salary_USD'].median():,.0f}")
print(f"  Salary range: ${df_proper['Current_Salary_USD'].min():,.0f} to ${df_proper['Current_Salary_USD'].max():,.0f}")
print(f"  Standard deviation: ${df_proper['Current_Salary_USD'].std():,.0f}")
print(f"  Interquartile range: ${df_proper['Current_Salary_USD'].quantile(0.25):,.0f} - ${df_proper['Current_Salary_USD'].quantile(0.75):,.0f}")

# Salary categories
print("\nSalary Category Distribution:")
salary_counts = df_proper['Salary_Category'].value_counts()
for category, count in salary_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {category}: {count} developers ({percentage:.1f}%)")

# Salary by experience level
print("\nAverage Salary by Experience Level:")
salary_by_exp = df_proper.groupby('Experience_Level')['Current_Salary_USD'].agg(['mean', 'median', 'count'])
for level in salary_by_exp.index:
    mean_salary = salary_by_exp.loc[level, 'mean']
    median_salary = salary_by_exp.loc[level, 'median']
    count = salary_by_exp.loc[level, 'count']
    print(f"  {level}:")
    print(f"    Average: ${mean_salary:,.0f}")
    print(f"    Median: ${median_salary:,.0f}")
    print(f"    Count: {count} developers")

# Salary by education level
print("\nAverage Salary by Education Level:")
salary_by_edu = df_proper.groupby('Education_Level')['Current_Salary_USD'].agg(['mean', 'median', 'count'])
for level in salary_by_edu.index:
    mean_salary = salary_by_edu.loc[level, 'mean']
    median_salary = salary_by_edu.loc[level, 'median']
    count = salary_by_edu.loc[level, 'count']
    print(f"  {level}:")
    print(f"    Average: ${mean_salary:,.0f}")
    print(f"    Median: ${median_salary:,.0f}")
    print(f"    Count: {count} developers")

# 6. PROGRAMMING PARADIGM LEARNING METRICS
print("\n\n6. PROGRAMMING PARADIGM LEARNING METRICS")
print("-" * 40)

# Paradigm difficulty ratings (1-10 scale)
print("\nParadigm Difficulty Ratings (1 = Easy, 10 = Difficult):")
difficulty_metrics = {}
for col in ['Imperative_Difficulty', 'Functional_Difficulty', 'Object_Oriented_Difficulty',
            'Logic_Difficulty', 'Reactive_Difficulty', 'Declarative_Difficulty']:
    mean_val = df_proper[col].mean()
    median_val = df_proper[col].median()
    std_val = df_proper[col].std()
    difficulty_metrics[col] = {
        'mean': mean_val,
        'median': median_val,
        'std': std_val,
        'min': df_proper[col].min(),
        'max': df_proper[col].max()
    }
    paradigm_name = col.replace('_', ' ').replace('Difficulty', '').strip()
    print(f"  {paradigm_name}:")
    print(f"    Mean: {mean_val:.2f}")
    print(f"    Median: {median_val:.2f}")
    print(f"    Std Dev: {std_val:.2f}")
    print(f"    Range: {df_proper[col].min():.0f} - {df_proper[col].max():.0f}")

# Average difficulty across all paradigms
print(f"\nOverall Average Difficulty: {df_proper['Avg_Difficulty'].mean():.2f}")
print(f"Overall Difficulty Range: {df_proper['Avg_Difficulty'].min():.2f} - {df_proper['Avg_Difficulty'].max():.2f}")

# Learning time in months
print("\nLearning Time to Proficiency (Months):")
learning_time_metrics = {}
for col in ['Imperative_Months', 'Functional_Months', 'Object_Oriented_Months',
            'Logic_Months', 'Reactive_Months', 'Declarative_Months']:
    mean_val = df_proper[col].mean()
    median_val = df_proper[col].median()
    std_val = df_proper[col].std()
    learning_time_metrics[col] = {
        'mean': mean_val,
        'median': median_val,
        'std': std_val
    }
    paradigm_name = col.replace('_', ' ').replace('Months', '').strip()
    print(f"  {paradigm_name}:")
    print(f"    Mean: {mean_val:.1f} months")
    print(f"    Median: {median_val:.1f} months")
    print(f"    Std Dev: {std_val:.1f} months")

# Total learning time
print(f"\nTotal Learning Time (All Paradigms):")
print(f"  Mean: {df_proper['Total_Learning_Months'].mean():.1f} months")
print(f"  Median: {df_proper['Total_Learning_Months'].median():.1f} months")
print(f"  Range: {df_proper['Total_Learning_Months'].min():.1f} - {df_proper['Total_Learning_Months'].max():.1f} months")

# 7. LEARNING PROCESS AND CHALLENGES
print("\n\n7. LEARNING PROCESS AND CHALLENGES")
print("-" * 40)

# Learning curve steepness
print("\nLearning Curve Steepness (1 = Gentle, 7 = Steep):")
print(f"  Mean: {df_proper['Learning_Curve_Steepness'].mean():.2f}")
print(f"  Median: {df_proper['Learning_Curve_Steepness'].median():.2f}")
print(f"  Range: {df_proper['Learning_Curve_Steepness'].min():.1f} - {df_proper['Learning_Curve_Steepness'].max():.1f}")

# Plateau experience
print("\nDevelopers Who Experienced Learning Plateaus:")
plateau_counts = df_proper['Plateau_Experienced'].value_counts()
for response, count in plateau_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {response}: {count} developers ({percentage:.1f}%)")

# Knowledge retention
print("\nKnowledge Retention (1 = Poor, 7 = Excellent):")
print(f"  Mean: {df_proper['Knowledge_Retention'].mean():.2f}")
print(f"  Median: {df_proper['Knowledge_Retention'].median():.2f}")
print(f"  Range: {df_proper['Knowledge_Retention'].min():.1f} - {df_proper['Knowledge_Retention'].max():.1f}")

# Difficulty transitioning between paradigms
print("\nDifficulty Transitioning Between Paradigms (1 = Easy, 7 = Difficult):")
print(f"  Mean: {df_proper['Difficulty_Transitioning'].mean():.2f}")
print(f"  Median: {df_proper['Difficulty_Transitioning'].median():.2f}")
print(f"  Range: {df_proper['Difficulty_Transitioning'].min():.1f} - {df_proper['Difficulty_Transitioning'].max():.1f}")

# Preference for first learned paradigm
print("\nPreference for First Learned Paradigm:")
pref_counts = df_proper['Prefer_First_Paradigm'].value_counts()
for response, count in pref_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {response}: {count} developers ({percentage:.1f}%)")

# Mental model shift required
print("\nMental Model Shift Required (1 = Minimal, 7 = Major):")
print(f"  Mean: {df_proper['Mental_Model_Shift'].mean():.2f}")
print(f"  Median: {df_proper['Mental_Model_Shift'].median():.2f}")
print(f"  Range: {df_proper['Mental_Model_Shift'].min():.1f} - {df_proper['Mental_Model_Shift'].max():.1f}")

# 8. LEARNING METHODS AND MOTIVATIONS
print("\n\n8. LEARNING METHODS AND MOTIVATIONS")
print("-" * 40)

# Preferred learning methods
print("\nTop 5 Preferred Learning Methods:")
learning_counts = df_proper['Preferred_Learning_Method'].value_counts().head(5)
for method, count in learning_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {method}: {count} developers ({percentage:.1f}%)")

# Motivation factors
print("\nTop 5 Motivation Factors for Learning Paradigms:")
motivation_counts = df_proper['Motivation_Factors'].value_counts().head(5)
for factor, count in motivation_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {factor}: {count} developers ({percentage:.1f}%)")

# Biggest challenges
print("\nTop 5 Biggest Challenges in Learning New Paradigms:")
challenge_counts = df_proper['Biggest_Challenge'].value_counts().head(5)
for challenge, count in challenge_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {challenge}: {count} developers ({percentage:.1f}%)")

# Transferable skills identified
print("\nTop 5 Most Valued Transferable Skills:")
skills_counts = df_proper['Transferable_Skills'].value_counts().head(5)
for skill, count in skills_counts.items():
    percentage = (count / len(df_proper)) * 100
    print(f"  {skill}: {count} developers ({percentage:.1f}%)")

# 9. PARADIGM DIVERSITY ANALYSIS
print("\n\n9. PARADIGM DIVERSITY ANALYSIS")
print("-" * 40)

print(f"\nParadigm Diversity Score (0-1 scale):")
print(f"  Mean: {df_proper['Paradigm_Diversity'].mean():.3f}")
print(f"  Median: {df_proper['Paradigm_Diversity'].median():.3f}")
print(f"  Range: {df_proper['Paradigm_Diversity'].min():.3f} - {df_proper['Paradigm_Diversity'].max():.3f}")

# Paradigm diversity by experience level
print("\nParadigm Diversity by Experience Level:")
diversity_by_exp = df_proper.groupby('Experience_Level')['Paradigm_Diversity'].agg(['mean', 'median', 'count'])
for level in diversity_by_exp.index:
    mean_div = diversity_by_exp.loc[level, 'mean']
    median_div = diversity_by_exp.loc[level, 'median']
    count = diversity_by_exp.loc[level, 'count']
    print(f"  {level}:")
    print(f"    Average diversity: {mean_div:.3f}")
    print(f"    Median diversity: {median_div:.3f}")
    print(f"    Count: {count} developers")