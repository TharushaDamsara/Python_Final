import json

# Load all notebook parts with UTF-8 encoding
with open('VHN_Readmission_Analysis.ipynb', 'r', encoding='utf-8') as f:
    part1 = json.load(f)

with open('notebook_part2.json', 'r', encoding='utf-8') as f:
    part2 = json.load(f)

with open('notebook_part3.json', 'r', encoding='utf-8') as f:
    part3 = json.load(f)

# Merge all cells
merged_notebook = part1.copy()
merged_notebook['cells'].extend(part2['cells'])
merged_notebook['cells'].extend(part3['cells'])

# Save merged notebook
with open('VHN_Readmission_Analysis_Complete.ipynb', 'w', encoding='utf-8') as f:
    json.dump(merged_notebook, f, indent=1, ensure_ascii=False)

print("✓ Notebook sections merged successfully!")
print(f"Total cells: {len(merged_notebook['cells'])}")
print(f"Saved as: VHN_Readmission_Analysis_Complete.ipynb")
