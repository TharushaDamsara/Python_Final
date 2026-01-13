# Strategic Patient Risk Stratification & Readmission Predictive Modeling
## Vitality Health Network (VHN) - Project Documentation

**Course:** ITS 2122: Python for Data Science & AI (Semester 3 – 2025)  
**Dataset:** Diabetes 130-US Hospitals (1999–2008)

---

## 📁 Project Structure

```
Python_Final/
├── data_files/
│   ├── diabetic_data.csv          # Main dataset
│   └── IDs_mapping.csv             # ID mappings for categorical variables
├── VHN_Readmission_Analysis_Complete.ipynb  # ⭐ MAIN JUPYTER NOTEBOOK
├── Strategic_Insight_Report.md    # ⭐ PROFESSIONAL BUSINESS REPORT
├── utils.py                        # Utility functions (VCI, scraping, visualization)
├── merge_notebook.py               # Script to merge notebook sections
└── README.md                       # This file
```

---

## 🎯 Project Overview

This project analyzes hospital readmission patterns among diabetic patients to help Vitality Health Network (VHN) reduce 30-day readmissions and avoid HRRP financial penalties.

**Key Deliverables:**
1. **Jupyter Notebook** - Complete technical implementation with all 4 phases
2. **Strategic Insight Report** - Professional business report (2,987 words)
3. **Utility Module** - Reusable Python functions

---

## 📊 Jupyter Notebook: VHN_Readmission_Analysis_Complete.ipynb

### Phase 1: Data Ingestion & Clinical Sanitation
- Load and audit dataset (101,766 patient encounters)
- Convert '?' placeholders to NaN
- Remove high-missingness columns (>90% threshold)
- Exclude deceased patients (2,192 patients)
- Convert categorical data types
- Remove duplicate records
- **Result:** Clean dataset ready for analysis

### Phase 2: Data Enrichment via Web Scraping
- Identify top 20 ICD-9 diagnosis codes
- Scrape ICD-9 descriptions from ICD9Data.com using BeautifulSoup
- Add `Primary_Diagnosis_Desc` column
- Implement ethical scraping (delays, headers, error handling)
- **Result:** Enhanced dataset with human-readable diagnoses

### Phase 3: Exploratory Data Analysis (EDA)
- **Class Imbalance:** 11% 30-day readmission rate
- **Demographics:** Age, gender, race patterns
- **Medications:** Insulin vs. oral vs. no medication analysis
- **Operational Metrics:** Time in hospital, lab procedures, medications
- **Correlations:** Heatmaps and correlation matrices
- **Result:** 15+ visualizations with clinical interpretations

### Phase 4: Feature Engineering - Vitality Complexity Index (VCI)
- **L:** Length of Stay (0-7 points)
- **A:** Acuity of Admission (0-3 points)
- **C:** Comorbidity Burden (0-5 points)
- **E:** Emergency Visits (0-5 points)
- **Risk Categories:** Low (0-6), Medium (7-12), High (≥13)
- **Validation:** High-risk patients show 2-2.5x higher readmission rates
- **Result:** Actionable risk stratification tool

---

## 📄 Strategic Insight Report: Strategic_Insight_Report.md

Professional business report structured for academic submission and viva defense:

### Sections:
1. **Executive Summary** - Key findings and recommendations
2. **Business & Healthcare Context** - HRRP challenges and VHN's imperative
3. **Data Methodology** - Dataset description, quality assessment, limitations
4. **Clinical & Operational Insights** - Demographic patterns, medication analysis, operational metrics
5. **VCI Explanation** - LACE-inspired framework, scoring logic, validation results
6. **Strategic Recommendations** - 6 actionable recommendations with implementation roadmap
7. **Conclusion** - Expected outcomes and success factors
8. **Appendices** - VCI calculation example, data quality summary, technical specs

**Word Count:** 2,987 words (within 2,500-3,000 target)

---

## 🛠️ Utility Module: utils.py

Reusable functions for healthcare analytics:

### Functions:
- `calculate_vci_score(row)` - Calculate VCI score for a patient
- `categorize_vci_risk(vci_score)` - Categorize into Low/Medium/High risk
- `scrape_icd9_description(icd9_code)` - Web scraping with ethical practices
- `audit_data_quality(df)` - Comprehensive data quality audit
- `print_audit_summary(audit_results)` - Formatted audit output
- `plot_readmission_by_category(df, category_col)` - Standardized visualizations
- `plot_readmission_rate_by_category(df, category_col)` - Rate comparisons
- `create_correlation_heatmap(df, columns)` - Correlation analysis

---

## 🚀 How to Run

### Prerequisites:
```bash
pip install pandas numpy matplotlib seaborn requests beautifulsoup4
```

### Step 1: Open Jupyter Notebook
```bash
jupyter notebook VHN_Readmission_Analysis_Complete.ipynb
```

### Step 2: Run All Cells
- Click "Kernel" → "Restart & Run All"
- Or run cells sequentially (Shift + Enter)

### Step 3: Review Outputs
- All visualizations will render inline
- VCI scores will be calculated and validated
- Enhanced dataset will be exported as `VHN_Enhanced_Dataset_with_VCI.csv`

### Step 4: Review Strategic Report
- Open `Strategic_Insight_Report.md` in any Markdown viewer
- Convert to PDF using Pandoc (optional):
  ```bash
  pandoc Strategic_Insight_Report.md -o Strategic_Insight_Report.pdf
  ```

---

## 📈 Key Findings

### 1. Readmission Rate
- **Overall 30-day readmission rate:** ~11%
- Below typical 15-20% benchmark for diabetic populations

### 2. Risk Stratification Performance
- **Low Risk (VCI 0-6):** 6-8% readmission rate
- **Medium Risk (VCI 7-12):** 10-12% readmission rate
- **High Risk (VCI ≥13):** 15-18% readmission rate
- **Risk Ratio:** 2.0-2.5x (High vs. Low)

### 3. Key Risk Factors
- **Age:** Patients 70+ show highest readmission rates
- **Medications:** Insulin users have 2-3% higher readmission rates
- **Length of Stay:** Longer stays correlate with readmission risk
- **Polypharmacy:** ≥15 medications increases complexity

### 4. Actionable Insights
- Target intensive interventions to high-risk patients (20-25% of population)
- Implement enhanced discharge protocols for insulin-dependent patients
- Focus on medication reconciliation for polypharmacy patients
- Address health equity disparities across racial/ethnic groups

---

## 🎓 Academic Submission Checklist

- ✅ **Jupyter Notebook:** Complete with all 4 phases, clear markdown, modular code
- ✅ **Strategic Report:** 2,987 words, professional tone, no code
- ✅ **Visualizations:** 15+ plots with clinical interpretations
- ✅ **Web Scraping:** Ethical practices implemented (delays, headers, error handling)
- ✅ **VCI Model:** Validated risk stratification (2-2.5x risk ratio)
- ✅ **Documentation:** Clear explanations suitable for viva defense
- ✅ **Reproducibility:** All code runs from clean kernel

---

## 🔬 Viva Defense Preparation

### Expected Questions & Answers:

**Q: Why did you remove deceased patients?**  
A: Deceased patients cannot be readmitted, so including them would artificially inflate the "no readmission" group and violate the clinical definition of readmission risk.

**Q: How does VCI differ from LACE?**  
A: VCI is inspired by LACE but adapted for diabetic populations. We use a composite comorbidity measure (diagnoses + procedures + medications) rather than Charlson Comorbidity Index, and we calibrated thresholds based on our specific dataset.

**Q: What is the clinical significance of the 2.5x risk ratio?**  
A: It means high-risk patients are 2.5 times more likely to be readmitted than low-risk patients, demonstrating strong discriminative ability and enabling efficient resource targeting.

**Q: How would you implement VCI in a real hospital?**  
A: Integrate VCI calculation into the EHR discharge workflow, create automated alerts for high-risk patients, establish tiered discharge protocols, and monitor performance prospectively.

**Q: What are the limitations of your analysis?**  
A: Data is from 1999-2008 (practice patterns may have changed), lacks socioeconomic variables, missing weight data (>95%), and we cannot validate VCI on contemporary VHN data.

**Q: Why use web scraping instead of a lookup table?**  
A: Web scraping demonstrates technical skills and ensures we get the most current ICD-9 descriptions from authoritative sources. It also shows ethical data collection practices.

---

## 📚 References & Resources

### Dataset Source:
- UCI Machine Learning Repository: Diabetes 130-US Hospitals (1999-2008)
- https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008

### ICD-9 Descriptions:
- ICD9Data.com: https://www.icd9data.com/

### LACE Index:
- van Walraven C, et al. (2010). "Derivation and validation of an index to predict early death or unplanned readmission after discharge from hospital to the community." CMAJ, 182(6), 551-557.

### HRRP Information:
- CMS Hospital Readmissions Reduction Program: https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/Readmissions-Reduction-Program

---

## 👥 Project Team

**Health Informatics Consulting Team**  
Course: ITS 2122 - Python for Data Science & AI  
Semester 3 – 2025

---

## 📝 License & Usage

This project is for educational purposes as part of the ITS 2122 course. The dataset is publicly available from UCI Machine Learning Repository. All analysis and recommendations are based on historical data and should be validated before clinical implementation.

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository for dataset access
- ICD9Data.com for medical coding references
- Course instructors for guidance and support

---

**Last Updated:** January 2026  
**Status:** Complete and ready for submission
# Python_Final
