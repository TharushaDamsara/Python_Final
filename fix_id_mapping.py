"""
Script to convert IDs_mapping.csv to proper format with Table column
"""
import pandas as pd

# Read the original file
with open('data_files/IDs_mapping.csv', 'r') as f:
    lines = f.readlines()

# Parse the file into structured data
all_data = []
current_table = None

for line in lines:
    line = line.strip()
    
    # Skip empty lines
    if not line or line == ',':
        current_table = None
        continue
    
    # Check if this is a header line (contains "description")
    if 'description' in line.lower():
        # Extract table name from previous context
        parts = line.split(',')
        if len(parts) >= 1:
            # The column name before "description" is the ID type
            current_table = parts[0]
        continue
    
    # Parse data lines
    if current_table and ',' in line:
        parts = line.split(',', 1)  # Split only on first comma
        if len(parts) == 2:
            id_value = parts[0].strip()
            description = parts[1].strip().strip('"')
            
            if id_value:  # Only add if ID is not empty
                all_data.append({
                    'Table': current_table,
                    'ID': id_value,
                    'Description': description
                })

# Create DataFrame
df_mapping = pd.DataFrame(all_data)

# Save to new file
df_mapping.to_csv('data_files/IDs_mapping_formatted.csv', index=False)

print(f"✓ Created formatted ID mapping file with {len(df_mapping)} entries")
print(f"\nTables included:")
for table in df_mapping['Table'].unique():
    count = len(df_mapping[df_mapping['Table'] == table])
    print(f"  • {table}: {count} mappings")
