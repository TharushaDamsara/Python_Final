import json

# Fix VHN_Readmission_Analysis_Complete.ipynb
with open('VHN_Readmission_Analysis_Complete.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'source' in cell:
        for i, line in enumerate(cell['source']):
            if "pd.read_csv('data_files/IDs_mapping.csv')" in line:
                cell['source'][i] = line.replace("data_files/IDs_mapping.csv", "data_files/IDs_mapping_formatted.csv")

with open('VHN_Readmission_Analysis_Complete.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✓ Fixed VHN_Readmission_Analysis_Complete.ipynb")
