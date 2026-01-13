import json
import re

# Fix VHN_Readmission_Analysis_Complete.ipynb indexing issue
with open('VHN_Readmission_Analysis_Complete.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed_count = 0
for cell in nb['cells']:
    if 'source' in cell:
        # Join lines to perform multiline matching if needed, but we'll work line by line mostly
        # We look for the pattern where apply() is followed by reindex() without unstack()
        
        # Strategy: find the end of the apply() block and ensure unstack() is there
        for i in range(len(cell['source'])):
            line = cell['source'][i]
            if "risk_readmit_analysis = df.groupby" in line:
                # We found the assignment. Now find the reindex call.
                for j in range(i, len(cell['source'])):
                    if ").reindex(risk_order)" in cell['source'][j] and ".unstack()" not in cell['source'][j]:
                        cell['source'][j] = cell['source'][j].replace(").reindex(risk_order)", ").unstack().reindex(risk_order)")
                        fixed_count += 1
                        print(f"✓ Fixed assignment starting at line {i} in cell source")
                        break

with open('VHN_Readmission_Analysis_Complete.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"✓ Total fixed occurrences: {fixed_count}")
