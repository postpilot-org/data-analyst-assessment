
#!/usr/bin/env python3
"""
Setup verification script for Data Analyst Technical Assessment
This script checks that all necessary files and data are in place
"""

import os
import sys
import pandas as pd
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✓ {description} found")
        return True
    else:
        print(f"✗ {description} missing - {filepath}")
        return False

def check_csv_data(filepath, expected_columns=None):
    """Validate CSV file can be read and has expected structure"""
    try:
        df = pd.read_csv(filepath)
        rows = len(df)
        cols = len(df.columns)
        print(f"  └─ {rows:,} rows, {cols} columns")
        
        if expected_columns:
            missing_cols = set(expected_columns) - set(df.columns)
            if missing_cols:
                print(f"  └─ ⚠ Missing columns: {missing_cols}")
                return False
        return True
    except Exception as e:
        print(f"  └─ ✗ Error reading file: {e}")
        return False

def main():
    print("=" * 60)
    print("Data Analyst Technical Assessment - Setup Verification")
    print("=" * 60)
    
    all_good = True
    
    # Check directory structure
    print("\n📁 Checking directory structure...")
    directories = ['data', 'question_1', 'question_2']
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"  Created directory: {dir_name}/")
    
    # Check for key files
    print("\n📄 Checking repository files...")
    files_to_check = [
        ('README.md', 'Main instructions'),
        ('requirements.txt', 'Python dependencies'),
        ('SQL_SETUP.sql', 'SQL setup instructions')
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check if data files exist
    print("\n📊 Checking datasets...")
    data_files = {
        'data/companies.csv': ['company_id', 'company_name', 'industry_category', 
                               'signup_date', 'monthly_budget'],
        'data/postcards.csv': ['id', 'size', 'cost_per_piece'],
        'data/campaigns.csv': ['campaign_id', 'company_id', 'campaign_name', 'mail_drop_date', 
                               'postcard_size', 'quantity_sent', 'holdout_size',
                               'campaign_type', 'test_group'],
        'data/orders.csv': ['order_id', 'company_id', 'customer_id', 'order_date', 
                           'order_amount', 'attribution_campaign_id', 'attribution_type', 
                           'days_from_mail_drop'],
        'data/holdout_orders.csv': ['company_id', 'campaign_id', 'holdout_period_start',
                                    'holdout_period_end', 'total_customers', 
                                    'total_orders', 'total_revenue'],
        'data/coupons.csv': ['coupon_code', 'coupon_name', 'discount_type', 
                            'discount_value', 'usage_type', 'max_uses',
                            'min_purchase_amount', 'valid_from', 'valid_until', 
                            'campaign_id'],
        'data/coupon_redemptions.csv': ['redemption_id', 'coupon_code', 'order_id',
                                       'customer_id', 'redemption_date', 
                                       'discount_applied'],
        'data/site_visits.csv': ['session_id', 'customer_id', 'company_id', 'visit_timestamp',
                                'pages_viewed', 'session_duration', 'traffic_source',
                                'converted', 'device_type']
    }
    
    data_exists = True
    for filepath, expected_cols in data_files.items():
        if check_file_exists(filepath, filepath):
            if not check_csv_data(filepath, expected_cols):
                data_exists = False
        else:
            data_exists = False
    
    if not data_exists:
        print("\n⚠ Some data files are missing or incomplete.")
        print("Please ensure you have cloned the repository correctly.")
        print("All data files should be included in the data/ directory.")
        all_good = False
    
    # Check Python environment
    print("\n🐍 Checking Python environment...")
    print(f"Python version: {sys.version.split()[0]}")
    
    required_packages = ['pandas', 'numpy', 'matplotlib', 'jupyter']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("Run 'pip install -r requirements.txt' to install dependencies.")
        all_good = False
    
    # Create template files if they don't exist
    print("\n📝 Checking assessment templates...")
    templates = {
        'question_1/part_a_benchmarks.sql': '-- Question 1 Part A: Industry Benchmarks\n-- Your SQL queries here\n',
        'question_1/part_b_dashboard.sql': '-- Question 1 Part B: Dashboard Queries\n-- Your SQL here\n',
        'question_1/analysis_summary.md': '# Campaign Performance Analysis\n\n## Part A: Benchmarks\n\n## Part B: Dashboard & Recommendations\n',
    }
    
    for filepath, content in templates.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  Created template: {filepath}")
    
    # Final status
    print("\n" + "=" * 60)
    if all_good:
        print("✅ Setup complete! You're ready to begin the assessment.")
        print("\nNext steps:")
        print("1. Load CSVs into your SQL database (see SQL_SETUP.sql)")
        print("2. Complete Exercise 1 & 2 using SQL")
        print("3. Complete Exercise 3 using Python/Jupyter")
        print("4. Submit your solutions via pull request")
    else:
        print("⚠ Setup incomplete. Please address the issues above.")
        print("\nIf you need to install Python packages, run:")
        print("  pip install -r requirements.txt")
        print("\nIf data files are missing, please re-clone the repository.")
    print("=" * 60)

if __name__ == "__main__":
    main()
