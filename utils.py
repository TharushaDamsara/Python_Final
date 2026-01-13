"""
Utility Functions for Vitality Health Network Readmission Analysis
Healthcare Analytics Project - ITS 2122

This module contains reusable functions for:
- VCI (Vitality Complexity Index) calculation
- ICD-9 code web scraping
- Data quality auditing
- Visualization helpers
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional


def calculate_vci_score(row: pd.Series) -> int:
    """
    Calculate Vitality Complexity Index (VCI) score for a patient.
    
    VCI is inspired by the LACE Index and includes:
    - L: Length of Stay (0-7 points)
    - A: Acuity of Admission (0-3 points)
    - C: Comorbidity Burden (0-5 points)
    - E: Emergency Visits (0-5 points)
    
    Parameters:
    -----------
    row : pd.Series
        Patient record containing required fields
        
    Returns:
    --------
    int : VCI score (0-20)
    """
    score = 0
    
    # L - Length of Stay
    time_in_hospital = row.get('time_in_hospital', 0)
    if time_in_hospital < 1:
        score += 0
    elif 1 <= time_in_hospital <= 4:
        score += 1
    elif 5 <= time_in_hospital <= 13:
        score += 4
    else:  # >= 14 days
        score += 7
    
    # A - Acuity of Admission
    admission_type = row.get('admission_type_id', 0)
    # Emergency (1) or Trauma (2) admissions are high acuity
    if admission_type in [1, 2]:
        score += 3
    
    # C - Comorbidity Burden
    # Count number of diagnoses (diag_1, diag_2, diag_3 that are not missing)
    diagnoses = [row.get('diag_1'), row.get('diag_2'), row.get('diag_3')]
    num_diagnoses = sum(1 for d in diagnoses if pd.notna(d) and d != '?')
    
    # Also consider number of procedures and medications as comorbidity indicators
    num_procedures = row.get('num_procedures', 0)
    num_medications = row.get('num_medications', 0)
    
    total_comorbidity = num_diagnoses + (num_procedures // 2) + (num_medications // 5)
    
    if total_comorbidity < 4:
        score += 0
    elif 4 <= total_comorbidity <= 7:
        score += 3
    else:  # >= 8
        score += 5
    
    # E - Emergency Visits
    # Using number_emergency as proxy for emergency visits
    emergency_visits = row.get('number_emergency', 0)
    if emergency_visits == 0:
        score += 0
    elif 1 <= emergency_visits <= 3:
        score += 3
    else:  # >= 4
        score += 5
    
    return score


def categorize_vci_risk(vci_score: int) -> str:
    """
    Categorize VCI score into risk groups.
    
    Parameters:
    -----------
    vci_score : int
        VCI score (0-20)
        
    Returns:
    --------
    str : Risk category ('Low', 'Medium', 'High')
    """
    if vci_score <= 6:
        return 'Low'
    elif 7 <= vci_score <= 12:
        return 'Medium'
    else:  # >= 13
        return 'High'


def scrape_icd9_description(icd9_code: str, delay: float = 0.5) -> str:
    """
    Scrape ICD-9 code description from ICD9Data.com.
    
    Implements ethical scraping practices:
    - User-agent header
    - Delay between requests
    - Error handling
    
    Parameters:
    -----------
    icd9_code : str
        ICD-9 code to look up
    delay : float
        Delay in seconds before making request (default: 0.5)
        
    Returns:
    --------
    str : Description of the ICD-9 code, or "Unknown" if not found
    """
    # Ethical scraping: add delay
    time.sleep(delay)
    
    # Clean the code
    code = str(icd9_code).strip()
    
    try:
        # Construct URL for ICD9Data.com
        url = f"https://www.icd9data.com/getICD9Code.ashx?icd9={code}"
        
        # Set user-agent header for ethical scraping
        headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Research Project)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the description
        # ICD9Data.com structure: look for specific elements
        description_elem = soup.find('h1', class_='pageTitle')
        
        if description_elem:
            # Extract text and clean it
            desc = description_elem.get_text(strip=True)
            # Remove the code itself from the description if present
            desc = desc.replace(code, '').strip(' -')
            return desc if desc else "Unknown"
        
        # Alternative: try to find in meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        return "Unknown"
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping ICD-9 code {code}: {e}")
        return "Unknown"
    except Exception as e:
        print(f"Unexpected error for code {code}: {e}")
        return "Unknown"


def audit_data_quality(df: pd.DataFrame) -> Dict:
    """
    Perform comprehensive data quality audit.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to audit
        
    Returns:
    --------
    dict : Data quality metrics
    """
    audit_results = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'duplicate_rows': df.duplicated().sum(),
        'missing_by_column': {},
        'high_missingness_columns': [],
        'data_types': df.dtypes.to_dict()
    }
    
    # Calculate missingness for each column
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        audit_results['missing_by_column'][col] = {
            'count': missing_count,
            'percentage': round(missing_pct, 2)
        }
        
        # Flag columns with >90% missingness
        if missing_pct > 90:
            audit_results['high_missingness_columns'].append(col)
    
    return audit_results


def plot_readmission_by_category(df: pd.DataFrame, category_col: str, 
                                  title: str = None, figsize: Tuple = (10, 6)):
    """
    Create standardized countplot for readmission analysis by category.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    category_col : str
        Column name to analyze
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    plt.figure(figsize=figsize)
    
    # Create countplot
    ax = sns.countplot(data=df, x=category_col, hue='readmitted', 
                       palette='Set2', order=df[category_col].value_counts().index)
    
    # Customize
    plt.title(title or f'Readmission by {category_col}', fontsize=14, fontweight='bold')
    plt.xlabel(category_col.replace('_', ' ').title(), fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Readmitted', loc='upper right')
    plt.tight_layout()
    
    return ax


def plot_readmission_rate_by_category(df: pd.DataFrame, category_col: str,
                                       title: str = None, figsize: Tuple = (10, 6)):
    """
    Plot readmission rate (percentage) by category.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    category_col : str
        Column name to analyze
    title : str
        Plot title
    figsize : tuple
        Figure size
    """
    # Calculate readmission rate
    readmit_rate = df.groupby(category_col)['readmitted'].apply(
        lambda x: (x == '<30').sum() / len(x) * 100
    ).sort_values(ascending=False)
    
    plt.figure(figsize=figsize)
    ax = readmit_rate.plot(kind='bar', color='steelblue', alpha=0.8)
    
    plt.title(title or f'30-Day Readmission Rate by {category_col}', 
              fontsize=14, fontweight='bold')
    plt.xlabel(category_col.replace('_', ' ').title(), fontsize=12)
    plt.ylabel('Readmission Rate (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.axhline(y=readmit_rate.mean(), color='red', linestyle='--', 
                label=f'Average: {readmit_rate.mean():.2f}%')
    plt.legend()
    plt.tight_layout()
    
    return ax


def create_correlation_heatmap(df: pd.DataFrame, columns: List[str] = None,
                               figsize: Tuple = (12, 10)):
    """
    Create correlation heatmap for numerical features.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    columns : list
        Specific columns to include (default: all numeric)
    figsize : tuple
        Figure size
    """
    if columns is None:
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
    else:
        numeric_df = df[columns]
    
    plt.figure(figsize=figsize)
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    
    plt.title('Correlation Matrix - Numerical Features', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return corr_matrix


def print_audit_summary(audit_results: Dict):
    """
    Print formatted data quality audit summary.
    
    Parameters:
    -----------
    audit_results : dict
        Results from audit_data_quality()
    """
    print("=" * 70)
    print("DATA QUALITY AUDIT SUMMARY")
    print("=" * 70)
    print(f"\nTotal Records: {audit_results['total_records']:,}")
    print(f"Total Columns: {audit_results['total_columns']}")
    print(f"Duplicate Rows: {audit_results['duplicate_rows']:,}")
    
    print("\n" + "-" * 70)
    print("HIGH MISSINGNESS COLUMNS (>90%)")
    print("-" * 70)
    if audit_results['high_missingness_columns']:
        for col in audit_results['high_missingness_columns']:
            pct = audit_results['missing_by_column'][col]['percentage']
            print(f"  • {col}: {pct:.2f}% missing")
    else:
        print("  None")
    
    print("\n" + "-" * 70)
    print("TOP 10 COLUMNS BY MISSINGNESS")
    print("-" * 70)
    sorted_missing = sorted(audit_results['missing_by_column'].items(),
                           key=lambda x: x[1]['percentage'], reverse=True)[:10]
    for col, stats in sorted_missing:
        print(f"  • {col}: {stats['percentage']:.2f}% ({stats['count']:,} records)")
    
    print("\n" + "=" * 70)
