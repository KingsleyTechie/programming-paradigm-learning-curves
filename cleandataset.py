print("\n=== CREATING CLEAN DATASET FROM SCRATCH ===")

# Let me first examine what we have in the good rows to understand the complete structure
print("\n=== COMPLETE COLUMN STRUCTURE FROM GOOD ROWS ===")
print("Columns in good rows:")
print(good_rows.columns.tolist())
print(f"\nNumber of columns in good rows: {len(good_rows.columns)}")

# Let's see the complete data types in good rows
print("\nData types in good rows:")
print(good_rows.dtypes)

# Now, let me create a new clean dataset by properly parsing the data
# The issue seems to be that the CSV was misaligned
# Let me try a different approach: read the CSV with different parameters

# First, let's save the current state and try to read the CSV properly
print("\n=== ATTEMPTING TO READ CSV WITH PROPER PARSING ===")

# Let me check if the issue is with delimiters or quotes
# First, let's read the raw data
import csv

# Read the raw CSV file
with open('/kaggle/input/learningcurves-csv/learningcurves.csv', 'r') as f:
    raw_data = f.read()

# Look at the first few lines
print("First 500 characters of raw CSV:")
print(raw_data[:500])

# Count lines
lines = raw_data.split('\n')
print(f"\nTotal lines in file: {len(lines)}")

# Look at line 25 (where the issue starts, 0-indexed)
print(f"\nLine 25 (where issues begin):")
print(lines[24])

# Look at line 24 (last good line)
print(f"\nLine 24 (last good line):")
print(lines[23])

# Count fields in each line
print("\n=== COUNTING FIELDS PER LINE ===")
for i in range(20, 30):
    fields = lines[i].split(',')
    print(f"Line {i}: {len(fields)} fields")
    if i == 23 or i == 24:
        print(f"  Sample: {fields[:5]}...")

# Now let me try to manually reconstruct the data
print("\n=== MANUALLY RECONSTRUCTING THE DATASET ===")

# Based on the pattern, I think the issue might be that some fields contain commas
# Let me try to read with proper quoting
try:
    df_fixed = pd.read_csv('/kaggle/input/learningcurves-csv/learningcurves.csv', 
                          quoting=csv.QUOTE_ALL,  # Treat all fields as quoted
                          engine='python')
    print("Successfully read with quoting!")
    print(f"Shape: {df_fixed.shape}")
    print(f"Columns: {len(df_fixed.columns)}")
except Exception as e:
    print(f"Error with quoting: {e}")

# Let me also try a different approach - read as raw and parse manually
print("\n=== PARSING DATA MANUALLY ===")

# Read all lines
all_rows = []
with open('/kaggle/input/learningcurves-csv/learningcurves.csv', 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        all_rows.append(row)
        if i < 5:  # Print first 5 rows
            print(f"Row {i}: {len(row)} fields - {row[:5]}...")

print(f"\nTotal rows read: {len(all_rows)}")

# Check field counts
field_counts = [len(row) for row in all_rows]
print(f"\nField counts: Min={min(field_counts)}, Max={max(field_counts)}, Avg={sum(field_counts)/len(field_counts):.1f}")

# Find rows with different field counts
print("\nRows with unusual field counts:")
for i, count in enumerate(field_counts):
    if count != 38:  # Should be 38 fields
        print(f"  Row {i}: {count} fields")