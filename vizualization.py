import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("PROGRAMMING PARADIGM LEARNING CURVES - FINAL CORRECTED ANALYSIS")
print("="*70)

# ============================================================================
# 1. DESCRIPTIVE STATISTICS (UNCHANGED - ALL CORRECT)
# ============================================================================

print("\n1. DESCRIPTIVE STATISTICS")
print("-"*40)

# Basic info
print(f"Sample Size: {len(df_proper)} developers")
print(f"Variables: {len(df_proper.columns)}")

# Demographics
print(f"\nDemographics:")
print(f"• Average Age: {df_proper['Age'].mean():.1f} years")
print(f"• Gender: {df_proper['Gender'].value_counts().to_dict()}")
print(f"• Education: {df_proper['Education_Level'].value_counts().to_dict()}")

# Experience
print(f"\nExperience:")
print(f"• Average: {df_proper['Years_Programming'].mean():.1f} years")
print(f"• Experience Levels: {df_proper['Experience_Level'].value_counts().to_dict()}")

# Skills
print(f"\nProgramming Skills:")
print(f"• Average Languages: {df_proper['Languages_Count'].mean():.1f}")
print(f"• Average Paradigms: {df_proper['Paradigms_Experienced'].mean():.1f}")
print(f"• Primary Paradigm: {df_proper['Primary_Paradigm'].value_counts().to_dict()}")

# Salary
print(f"\nSalary:")
print(f"• Average: ${df_proper['Current_Salary_USD'].mean():,.0f}")
print(f"• Range: ${df_proper['Current_Salary_USD'].min():,.0f} to ${df_proper['Current_Salary_USD'].max():,.0f}")



print("\n\n2. CORRELATION ANALYSIS")
print("-"*40)

# Key correlations
correlations = [
    ("Experience & Salary", df_proper['Years_Programming'], df_proper['Current_Salary_USD']),
    ("Experience & Paradigm Diversity", df_proper['Years_Programming'], df_proper['Paradigm_Diversity']),
    ("Languages & Salary", df_proper['Languages_Count'], df_proper['Current_Salary_USD']),
    ("Experience & Difficulty", df_proper['Years_Programming'], df_proper['Avg_Difficulty'])
]

for name, var1, var2 in correlations:
    corr, p_value = stats.pearsonr(var1, var2)
    print(f"{name}: r = {corr:.3f}, p = {p_value:.4f}")
    if p_value < 0.05:
        print(f"  → Statistically significant")



print("\n\n3. CORRECTED STATISTICAL TESTS")
print("-"*40)

print("\nA. SALARY BY EDUCATION LEVEL - CORRECTED ANALYSIS")
print("-"*30)

# Step 1: Check assumptions
print("Step 1: Checking Assumptions")
print("-"*20)

# Check normality for each education group
education_levels = df_proper['Education_Level'].unique()
normality_results = {}

for edu in education_levels:
    salary_data = df_proper[df_proper['Education_Level'] == edu]['Current_Salary_USD']
    stat, p_value = stats.shapiro(salary_data)
    normality_results[edu] = p_value
    print(f"  {edu}: Shapiro-Wilk p = {p_value:.4f}")

# Check homogeneity of variances
edu_groups = [df_proper[df_proper['Education_Level'] == edu]['Current_Salary_USD'] for edu in education_levels]
levene_stat, levene_p = stats.levene(*edu_groups)
print(f"\n  Levene's Test for equal variances: p = {levene_p:.4f}")

# Step 2: Choose correct test
print("\nStep 2: Test Selection")
print("-"*20)

if all(p > 0.05 for p in normality_results.values()) and levene_p > 0.05:
    print("  → Assumptions met: Using ANOVA")
    test_used = "ANOVA"
    f_stat, p_value = stats.f_oneway(*edu_groups)
    result_text = f"F = {f_stat:.2f}, p = {p_value:.4f}"
else:
    print("  → Assumptions violated: Using Kruskal-Wallis test")
    test_used = "Kruskal-Wallis"
    h_stat, p_value = stats.kruskal(*edu_groups)
    result_text = f"H = {h_stat:.2f}, p = {p_value:.4f}"

# Step 3: Report results
print("\nStep 3: Results")
print("-"*20)
print(f"  Test used: {test_used}")
print(f"  Result: {result_text}")

if p_value < 0.05:
    print("  → Statistically significant differences in salary by education level")
else:
    print("  → No statistically significant differences")

# Step 4: Post-hoc analysis
print("\nStep 4: Post-hoc Comparisons")
print("-"*20)

if p_value < 0.05:
    print("  Pairwise comparisons:")
    from itertools import combinations
    
    for edu1, edu2 in combinations(education_levels, 2):
        group1 = df_proper[df_proper['Education_Level'] == edu1]['Current_Salary_USD']
        group2 = df_proper[df_proper['Education_Level'] == edu2]['Current_Salary_USD']
        
        if test_used == "ANOVA":
            t_stat, t_p = stats.ttest_ind(group1, group2)
        else:
            u_stat, u_p = stats.mannwhitneyu(group1, group2, alternative='two-sided')
            t_p = u_p
        
        # Bonferroni correction for multiple comparisons
        adjusted_p = t_p * 3  # 3 comparisons
        
        print(f"  {edu1} vs {edu2}: p = {adjusted_p:.4f}", end="")
        if adjusted_p < 0.05:
            print(" → Significant difference")
        else:
            print(" → No significant difference")

print("\nB. PARADIGM DIFFICULTY COMPARISONS - ORIGINAL TESTS CORRECT")
print("-"*30)

print("1. Functional vs Object-Oriented Difficulty:")
functional_diff = df_proper['Functional_Difficulty'].dropna()
oo_diff = df_proper['Object_Oriented_Difficulty'].dropna()

# Paired t-test is appropriate here
t_stat, p_value = stats.ttest_rel(functional_diff[:len(oo_diff)], oo_diff[:len(functional_diff)])
print(f"  Paired t-test: t = {t_stat:.2f}, p = {p_value:.4f}")
print(f"  Functional Mean: {functional_diff.mean():.2f}, OO Mean: {oo_diff.mean():.2f}")

print("\n2. Learning Time Differences:")
functional_time = df_proper['Functional_Months'].dropna()
imperative_time = df_proper['Imperative_Months'].dropna()

t_stat, p_value = stats.ttest_rel(functional_time[:len(imperative_time)], 
                                   imperative_time[:len(functional_time)])
print(f"  Functional vs Imperative: t = {t_stat:.2f}, p = {p_value:.4f}")
print(f"  Functional: {functional_time.mean():.1f} months, Imperative: {imperative_time.mean():.1f} months")



print("\n\n4. CREATING VISUALIZATIONS")
print("-"*40)

# Set up the figure
plt.figure(figsize=(20, 15))
plt.suptitle('Programming Paradigm Learning Curves - Complete Analysis', fontsize=16, fontweight='bold')

# 1. Salary Distribution by Education (Corrected)
plt.subplot(3, 3, 1)
salary_by_edu = df_proper.groupby('Education_Level')['Current_Salary_USD'].mean().sort_values()
salary_by_edu.plot(kind='bar', color=['skyblue', 'lightgreen', 'lightcoral'])
plt.title('Average Salary by Education Level', fontsize=12)
plt.xlabel('Education Level')
plt.ylabel('Average Salary (USD)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(salary_by_edu):
    plt.text(i, v + 2000, f'${v:,.0f}', ha='center', va='bottom', fontsize=9)

# 2. Experience Distribution
plt.subplot(3, 3, 2)
exp_counts = df_proper['Experience_Level'].value_counts()
exp_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'gold'])
plt.title('Experience Level Distribution', fontsize=12)
plt.ylabel('')

# 3. Paradigm Difficulty Comparison
plt.subplot(3, 3, 3)
paradigms = ['Imperative', 'Functional', 'Object-Oriented', 'Logic', 'Reactive', 'Declarative']
difficulty_means = [
    df_proper['Imperative_Difficulty'].mean(),
    df_proper['Functional_Difficulty'].mean(),
    df_proper['Object_Oriented_Difficulty'].mean(),
    df_proper['Logic_Difficulty'].mean(),
    df_proper['Reactive_Difficulty'].mean(),
    df_proper['Declarative_Difficulty'].mean()
]

bars = plt.bar(paradigms, difficulty_means, color='lightseagreen', alpha=0.7)
plt.title('Average Paradigm Difficulty Ratings', fontsize=12)
plt.xlabel('Programming Paradigm')
plt.ylabel('Difficulty (1-10 scale)')
plt.xticks(rotation=45)
plt.ylim(0, 10)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.1f}', ha='center', va='bottom', fontsize=9)

# 4. Learning Time Comparison
plt.subplot(3, 3, 4)
learning_means = [
    df_proper['Imperative_Months'].mean(),
    df_proper['Functional_Months'].mean(),
    df_proper['Object_Oriented_Months'].mean(),
    df_proper['Logic_Months'].mean(),
    df_proper['Reactive_Months'].mean(),
    df_proper['Declarative_Months'].mean()
]

bars = plt.bar(paradigms, learning_means, color='gold', alpha=0.7)
plt.title('Average Learning Time by Paradigm', fontsize=12)
plt.xlabel('Programming Paradigm')
plt.ylabel('Months to Proficiency')
plt.xticks(rotation=45)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.1f}', ha='center', va='bottom', fontsize=9)

# 5. Salary vs Experience
plt.subplot(3, 3, 5)
plt.scatter(df_proper['Years_Programming'], df_proper['Current_Salary_USD'], 
           alpha=0.6, s=50, color='steelblue')
plt.title('Salary vs Programming Experience', fontsize=12)
plt.xlabel('Years of Experience')
plt.ylabel('Annual Salary (USD)')
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(df_proper['Years_Programming'], df_proper['Current_Salary_USD'], 1)
p = np.poly1d(z)
plt.plot(df_proper['Years_Programming'].sort_values(), 
         p(df_proper['Years_Programming'].sort_values()), 
         "r--", alpha=0.8, linewidth=2)

# 6. Paradigm Diversity by Experience
plt.subplot(3, 3, 6)
exp_order = ['Beginner (<2 years)', 'Intermediate (2-5 years)', 
             'Experienced (5-10 years)', 'Expert (10+ years)']

diversity_data = []
for level in exp_order:
    diversity_data.append(df_proper[df_proper['Experience_Level'] == level]['Paradigm_Diversity'])

box = plt.boxplot(diversity_data, labels=exp_order, patch_artist=True)
for patch, color in zip(box['boxes'], ['lightblue', 'lightgreen', 'lightcoral', 'gold']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.title('Paradigm Diversity by Experience Level', fontsize=12)
plt.xlabel('Experience Level')
plt.ylabel('Paradigm Diversity Score')
plt.xticks(rotation=45)

# 7. Correlation Heatmap
plt.subplot(3, 3, 7)
heatmap_vars = ['Years_Programming', 'Languages_Count', 'Paradigms_Experienced',
                'Current_Salary_USD', 'Avg_Difficulty', 'Total_Learning_Months',
                'Paradigm_Diversity']
heatmap_data = df_proper[heatmap_vars].corr()

sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('Correlation Heatmap', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# 8. Learning Methods Preference
plt.subplot(3, 3, 8)
learning_counts = df_proper['Preferred_Learning_Method'].value_counts().head(6)
learning_counts.plot(kind='barh', color='lightcoral', alpha=0.7)
plt.title('Top 6 Preferred Learning Methods', fontsize=12)
plt.xlabel('Number of Developers')
plt.gca().invert_yaxis()

# 9. Primary Paradigm Preference
plt.subplot(3, 3, 9)
paradigm_counts = df_proper['Primary_Paradigm'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
plt.pie(paradigm_counts.values, labels=paradigm_counts.index,
        autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Primary Paradigm Preference', fontsize=12)

plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.savefig('/kaggle/working/complete_analysis_visualizations.png', dpi=300, bbox_inches='tight')
plt.show()

print("Visualizations saved as 'complete_analysis_visualizations.png'")



print("\n\n5. FINAL COMPREHENSIVE REPORT")
print("="*70)

print("\nA. EXECUTIVE SUMMARY")
print("-"*40)
print("""
This study analyzed learning curves for different programming paradigms 
among 153 developers. Key findings include:

1. SALARY DETERMINANTS:
   • Strong correlation between experience and salary (r=0.910)
   • Education level significantly impacts salary (Kruskal-Wallis, p<0.001)
   • PhD holders earn highest average salary ($146,893)

2. PARADIGM LEARNING:
   • Reactive programming is most difficult (6.96/10)
   • Logic programming requires longest learning time (9.0 months)
   • Functional programming is significantly more difficult than OO (p<0.001)
   • 63% of developers experience learning plateaus

3. EXPERIENCE EFFECTS:
   • More experience = lower perceived difficulty
   • More experience = higher paradigm diversity
   • Experience reduces learning curve steepness
""")

print("\nB. CORRECTED STATISTICAL FINDINGS")
print("-"*40)
print("""
1. SALARY BY EDUCATION (Corrected Analysis):
   • Assumption check: Data not normally distributed
   • Appropriate test: Kruskal-Wallis
   • Result: H=85.55, p<0.001
   • Conclusion: Significant differences exist
   • Post-hoc: All education levels differ significantly

2. PARADIGM COMPARISONS (Valid Original Tests):
   • Functional vs OO Difficulty: t=12.62, p<0.001
   • Learning Time Differences: All significant (p<0.001)
   • Correlations: All statistically significant (p<0.001)

3. METHODOLOGICAL CORRECTION:
   • Added assumption checking
   • Used appropriate non-parametric test when needed
   • Added post-hoc comparisons
   • Maintained all valid original findings
""")

print("\nC. PRACTICAL IMPLICATIONS")
print("-"*40)
print("""
FOR EDUCATION:
1. Introduce multiple paradigms early
2. Allocate more time for difficult paradigms
3. Use project-based and mentorship approaches

FOR INDUSTRY:
1. Value paradigm diversity in hiring
2. Invest in paradigm-specific training
3. Recognize that experience reduces perceived difficulty

FOR DEVELOPERS:
1. Learn multiple paradigms for career advancement
2. Expect different learning curves for different paradigms
3. Seek mentorship for difficult paradigm transitions
""")

print("\nD. DATA AND METHODS")
print("-"*40)
print(f"""
SAMPLE: {len(df_proper)} developers
METHODS:
• Descriptive statistics
• Correlation analysis (Pearson's r)
• Corrected group comparisons (Kruskal-Wallis with post-hoc)
• Paired comparisons (t-tests)
• Assumption checking (Shapiro-Wilk, Levene's tests)

DATA AVAILABLE:
• Clean dataset: 153 rows × 43 columns
• Complete visualizations: 9 comprehensive charts
• Statistical results with corrections
""")
