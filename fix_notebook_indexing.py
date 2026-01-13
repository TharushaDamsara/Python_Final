import json

# Fix VHN_Readmission_Analysis_Complete.ipynb indexing issue
with open('VHN_Readmission_Analysis_Complete.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'source' in cell:
        source_text = "".join(cell['source'])
        if "risk_readmit_analysis = df.groupby('VCI_Risk_Category')['readmitted'].apply(" in source_text:
            # Find the specific lines and insert .unstack()
            for i, line in enumerate(cell['source']):
                if ").reindex(risk_order)" in line:
                    cell['source'][i] = line.replace(").reindex(risk_order)", ").unstack().reindex(risk_order)")
                    print("✓ Applied .unstack() fix to cell")

with open('VHN_Readmission_Analysis_Complete.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✓ Fixed VHN_Readmission_Analysis_Complete.ipynb indexing issue")
