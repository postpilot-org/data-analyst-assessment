"""
Generate sample datasets for Data Analyst Assessment
Creates realistic direct mail marketing datasets with holdout groups for incrementality testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

print("Generating datasets for direct mail marketing company...")
print("=" * 50)

# Shopify industry categories (realistic selection)
SHOPIFY_INDUSTRIES = [
    'Clothing and Apparel', 'Health and Beauty', 'Home and Garden',
    'Electronics and Gadgets', 'Food and Beverage', 'Sports and Recreation',
    'Jewelry and Accessories', 'Pet Supplies', 'Toys and Games',
    'Arts and Entertainment', 'Automotive', 'Baby and Kids',
    'Books and Media', 'Office Supplies', 'Tools and Hardware',
    'Furniture', 'Fitness and Wellness', 'Outdoor and Camping',
    'Shoes and Footwear', 'Crafts and Hobbies'
]

# Helper functions
def generate_company_name(industry):
    """Generate realistic company names based on industry"""
    prefixes = {
        'Clothing and Apparel': ['Urban', 'Classic', 'Modern', 'Vintage', 'Elite'],
        'Health and Beauty': ['Pure', 'Glow', 'Radiant', 'Natural', 'Wellness'],
        'Home and Garden': ['Cozy', 'Green', 'Haven', 'Nest', 'Bloom'],
        'Electronics and Gadgets': ['Tech', 'Smart', 'Digital', 'Cyber', 'Future'],
        'Food and Beverage': ['Fresh', 'Artisan', 'Gourmet', 'Organic', 'Harvest'],
        'Pet Supplies': ['Happy', 'Paw', 'Pet', 'Furry', 'Tail'],
        'Toys and Games': ['Fun', 'Play', 'Joy', 'Magic', 'Wonder'],
        'Fitness and Wellness': ['Fit', 'Active', 'Strong', 'Vital', 'Peak']
    }
    
    suffixes = {
        'Clothing and Apparel': ['Threads', 'Boutique', 'Style', 'Wardrobe', 'Fashion'],
        'Health and Beauty': ['Beauty', 'Cosmetics', 'Skincare', 'Spa', 'Essentials'],
        'Home and Garden': ['Home', 'Living', 'Gardens', 'Decor', 'Interiors'],
        'Electronics and Gadgets': ['Hub', 'Store', 'Zone', 'World', 'Solutions'],
        'Food and Beverage': ['Market', 'Kitchen', 'Pantry', 'Foods', 'Co'],
        'Pet Supplies': ['Pals', 'Friends', 'Paradise', 'World', 'Supply'],
        'Toys and Games': ['Toys', 'Games', 'Land', 'Shop', 'Store'],
        'Fitness and Wellness': ['Fitness', 'Gym', 'Athletics', 'Performance', 'Health']
    }
    
    # Get prefixes and suffixes for the industry, with fallback
    prefix_list = prefixes.get(industry, ['Quality', 'Premium', 'Best', 'Top', 'Great'])
    suffix_list = suffixes.get(industry, ['Store', 'Shop', 'Co', 'Direct', 'Online'])
    
    return f"{random.choice(prefix_list)} {random.choice(suffix_list)}"

def generate_coupon_code(prefix=""):
    """Generate realistic coupon codes"""
    if prefix:
        return f"{prefix}{random.randint(10, 99)}"
    prefixes = ['SAVE', 'DEAL', 'SALE', 'OFFER', 'PROMO', 'WELCOME', 'VIP', 'FLASH']
    return f"{random.choice(prefixes)}{random.randint(10, 99)}"

# 1. Generate postcards.csv (fixed costs table)
print("\n1. Generating postcards.csv...")
postcards = pd.DataFrame({
    'id': ['PC1', 'PC2', 'PC3', 'PC4', 'PC5'],
    'size': ['4x6', '5x7', '6x9', '6x11', '9x12'],
    'cost_per_piece': [0.45, 0.58, 0.72, 0.89, 1.25]  # Including production and postage
})
postcards.to_csv('data/postcards.csv', index=False)
print(f"✓ Created {len(postcards)} postcard sizes")

# 2. Generate companies.csv
print("\n2. Generating companies.csv...")
num_companies = 150
company_ids = [f'COMP{str(i).zfill(4)}' for i in range(1, num_companies + 1)]

companies_data = []
for i, company_id in enumerate(company_ids):
    industry = random.choice(SHOPIFY_INDUSTRIES)
    company = {
        'company_id': company_id,
        'company_name': generate_company_name(industry),
        'industry_category': industry,
        'signup_date': datetime.now() - timedelta(days=random.randint(90, 730)),
        'monthly_budget': round(random.choice([5000, 10000, 15000, 25000, 50000, 75000, 100000]) * 
                               random.uniform(0.8, 1.2), 2)
    }
    companies_data.append(company)

companies = pd.DataFrame(companies_data)
companies.to_csv('data/companies.csv', index=False)
print(f"✓ Created {len(companies)} client companies across {len(SHOPIFY_INDUSTRIES)} industries")

# 3. Generate campaigns.csv
print("\n3. Generating campaigns.csv...")

num_campaigns = 500  # More campaigns since we have many companies
campaigns_data = []
campaign_counter = 1

# Generate campaigns over the past 18 months
start_date = datetime.now() - timedelta(days=540)

for company in companies.itertuples():
    # Each company runs 2-8 campaigns
    num_company_campaigns = random.randint(2, 8)
    
    for _ in range(num_company_campaigns):
        campaign_date = start_date + timedelta(days=random.randint(0, 540))
        
        # Vary quantity by company budget
        base_quantity = int(company.monthly_budget / 50)  # Rough estimate
        quantity = random.randint(base_quantity * 5, base_quantity * 20)
        
        campaign = {
            'campaign_id': f'C{campaign_counter:05d}',
            'company_id': company.company_id,
            'campaign_name': f"{random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'Holiday'])} "
                           f"{random.choice(['Sale', 'Promo', 'Launch', 'Special'])} "
                           f"{campaign_date.year}",
            'mail_drop_date': campaign_date,
            'postcard_size': random.choice(['PC1', 'PC2', 'PC3', 'PC4', 'PC5']),
            'quantity_sent': quantity,
            'holdout_size': int(quantity * 0.1),  # 10% holdout group
            'campaign_type': random.choice(['acquisition', 'retention', 'winback', 'seasonal']),
            'test_group': random.choice(['control', 'variant_a', 'variant_b'])
        }
        campaigns_data.append(campaign)
        campaign_counter += 1
        
        if campaign_counter > num_campaigns:
            break
    
    if campaign_counter > num_campaigns:
        break

campaigns = pd.DataFrame(campaigns_data[:num_campaigns])
campaigns.to_csv('data/campaigns.csv', index=False)
print(f"✓ Created {len(campaigns)} campaigns")

# 4. Generate orders.csv (treatment group orders)
print("\n4. Generating orders.csv...")

orders_data = []
order_id_counter = 10000
customer_id_counter = 1

# Industry-specific response rates
industry_response_rates = {
    'Clothing and Apparel': 0.025,
    'Health and Beauty': 0.032,
    'Home and Garden': 0.018,
    'Electronics and Gadgets': 0.015,
    'Food and Beverage': 0.045,
    'Pet Supplies': 0.038,
    'Toys and Games': 0.028,
    'Fitness and Wellness': 0.022,
    'Jewelry and Accessories': 0.012,
    'Sports and Recreation': 0.020
}

for _, campaign in campaigns.iterrows():
    # Get company industry for response rate
    company = companies[companies['company_id'] == campaign['company_id']].iloc[0]
    base_rate = industry_response_rates.get(company['industry_category'], 0.025)
    
    # Adjust for campaign type
    type_multipliers = {
        'acquisition': 0.5,
        'retention': 2.5,
        'winback': 1.5,
        'seasonal': 3.0
    }
    base_rate *= type_multipliers.get(campaign['campaign_type'], 1.0)
    
    # A/B test lift
    if campaign['test_group'] == 'variant_a':
        response_rate = base_rate * random.uniform(1.05, 1.15)
    elif campaign['test_group'] == 'variant_b':
        response_rate = base_rate * random.uniform(1.10, 1.25)
    else:
        response_rate = base_rate
    
    # Calculate actual number of orders
    num_orders = int(campaign['quantity_sent'] * response_rate * random.uniform(0.9, 1.1))
    
    for _ in range(num_orders):
        # Generate customer ID specific to company
        customer_id = f"{campaign['company_id']}_CUST{customer_id_counter:06d}"
        customer_id_counter += 1
        
        # Order timing - gamma distribution for realistic delay
        days_to_order = min(int(np.random.gamma(2.5, 3.2)), 45)
        order_date = campaign['mail_drop_date'] + timedelta(days=days_to_order)
        
        # Order amount varies by industry
        industry_aov = {
            'Clothing and Apparel': 85,
            'Health and Beauty': 65,
            'Home and Garden': 120,
            'Electronics and Gadgets': 250,
            'Food and Beverage': 45,
            'Pet Supplies': 55,
            'Toys and Games': 40,
            'Fitness and Wellness': 95,
            'Jewelry and Accessories': 150,
            'Sports and Recreation': 110
        }
        base_aov = industry_aov.get(company['industry_category'], 75)
        order_amount = max(15, np.random.lognormal(np.log(base_aov), 0.4))
        
        order = {
            'order_id': f'ORD{order_id_counter:08d}',
            'company_id': campaign['company_id'],
            'customer_id': customer_id,
            'order_date': order_date,
            'order_amount': round(order_amount, 2),
            'attribution_campaign_id': campaign['campaign_id'],
            'attribution_type': np.random.choice(['direct', 'assisted', 'view_through'], 
                                                p=[0.7, 0.25, 0.05]),
            'days_from_mail_drop': days_to_order
        }
        orders_data.append(order)
        order_id_counter += 1

orders = pd.DataFrame(orders_data)
orders.to_csv('data/orders.csv', index=False)
print(f"✓ Created {len(orders)} treatment group orders")

# 5. Generate holdout_orders.csv
print("\n5. Generating holdout_orders.csv...")

holdout_data = []

for _, campaign in campaigns.iterrows():
    # Get company for industry-specific behavior
    company = companies[companies['company_id'] == campaign['company_id']].iloc[0]
    
    # Holdout group has natural purchase rate (no campaign influence)
    natural_rate = industry_response_rates.get(company['industry_category'], 0.025) * 0.3
    
    # Seasonal adjustment (higher natural rate during seasonal campaigns)
    if campaign['campaign_type'] == 'seasonal':
        natural_rate *= 1.5
    
    holdout_customers = campaign['holdout_size']
    holdout_orders_count = int(holdout_customers * natural_rate * random.uniform(0.8, 1.2))
    
    # Calculate revenue based on typical AOV for the industry
    industry_aov = {
        'Clothing and Apparel': 85,
        'Health and Beauty': 65,
        'Home and Garden': 120,
        'Electronics and Gadgets': 250,
        'Food and Beverage': 45,
        'Pet Supplies': 55,
        'Toys and Games': 40,
        'Fitness and Wellness': 95,
        'Jewelry and Accessories': 150,
        'Sports and Recreation': 110
    }
    avg_order_value = industry_aov.get(company['industry_category'], 75)
    
    holdout_revenue = holdout_orders_count * avg_order_value * random.uniform(0.9, 1.1)
    
    holdout = {
        'company_id': campaign['company_id'],
        'campaign_id': campaign['campaign_id'],
        'holdout_period_start': campaign['mail_drop_date'],
        'holdout_period_end': campaign['mail_drop_date'] + timedelta(days=30),
        'total_customers': holdout_customers,
        'total_orders': holdout_orders_count,
        'total_revenue': round(holdout_revenue, 2)
    }
    holdout_data.append(holdout)

holdout_orders = pd.DataFrame(holdout_data)
holdout_orders.to_csv('data/holdout_orders.csv', index=False)
print(f"✓ Created {len(holdout_orders)} holdout group records")

# 6. Generate coupons.csv
print("\n6. Generating coupons.csv...")

coupons_list = []
coupon_codes_all = []

for idx, campaign in campaigns.iterrows():
    # Each campaign has 1-3 coupons
    num_coupons = random.randint(1, 3)
    
    for i in range(num_coupons):
        # Generate unique coupon code
        if campaign['campaign_type'] == 'acquisition':
            code = generate_coupon_code('NEW')
        elif campaign['campaign_type'] == 'winback':
            code = generate_coupon_code('COMEBACK')
        else:
            code = generate_coupon_code()
        
        # Ensure unique
        while code in coupon_codes_all:
            code = generate_coupon_code() + str(random.randint(100, 999))
        coupon_codes_all.append(code)
        
        # Determine discount type and value
        if i == 0:  # Primary coupon
            discount_type = np.random.choice(['percentage', 'fixed_amount'], p=[0.7, 0.3])
            if discount_type == 'percentage':
                discount_value = random.choice([10, 15, 20, 25, 30])
            else:
                discount_value = random.choice([5, 10, 15, 20, 25])
        elif i == 1:  # Secondary coupon
            discount_type = np.random.choice(['free_shipping', 'percentage'], p=[0.6, 0.4])
            discount_value = 0 if discount_type == 'free_shipping' else random.choice([10, 15])
        else:  # Tertiary coupon
            discount_type = 'bogo'
            discount_value = 50
        
        coupon = {
            'coupon_code': code,
            'coupon_name': f"{code} - Campaign {campaign['campaign_id']}",
            'discount_type': discount_type,
            'discount_value': discount_value,
            'usage_type': np.random.choice(['single_use', 'multi_use', 'static'], p=[0.2, 0.3, 0.5]),
            'max_uses': random.choice([1, 100, 1000, 10000]) if random.random() > 0.3 else None,
            'min_purchase_amount': random.choice([0, 25, 50, 75, 100]) if random.random() > 0.5 else 0,
            'valid_from': campaign['mail_drop_date'],
            'valid_until': campaign['mail_drop_date'] + timedelta(days=random.randint(30, 90)),
            'campaign_id': campaign['campaign_id']
        }
        coupons_list.append(coupon)

coupons = pd.DataFrame(coupons_list)
coupons.to_csv('data/coupons.csv', index=False)
print(f"✓ Created {len(coupons)} coupons")

# 7. Generate coupon_redemptions.csv
print("\n7. Generating coupon_redemptions.csv...")

redemptions_list = []
redemption_id_counter = 1

# 60% of orders use a coupon
orders_with_coupons = orders.sample(frac=0.60)

for _, order in orders_with_coupons.iterrows():
    # Get coupons for this campaign
    campaign_coupons = coupons[coupons['campaign_id'] == order['attribution_campaign_id']]
    
    if len(campaign_coupons) > 0:
        # Choose a coupon (usually the primary one)
        if random.random() < 0.7 and len(campaign_coupons) > 0:
            coupon = campaign_coupons.iloc[0]
        else:
            coupon = campaign_coupons.sample(1).iloc[0]
        
        # Calculate actual discount applied
        if coupon['discount_type'] == 'percentage':
            discount_applied = order['order_amount'] * (coupon['discount_value'] / 100)
        elif coupon['discount_type'] == 'fixed_amount':
            discount_applied = min(coupon['discount_value'], order['order_amount'])
        elif coupon['discount_type'] == 'free_shipping':
            discount_applied = random.uniform(5, 15)
        else:  # BOGO
            discount_applied = order['order_amount'] * 0.25
        
        redemption = {
            'redemption_id': f'RDM{redemption_id_counter:08d}',
            'coupon_code': coupon['coupon_code'],
            'order_id': order['order_id'],
            'customer_id': order['customer_id'],
            'redemption_date': order['order_date'],
            'discount_applied': round(discount_applied, 2)
        }
        redemptions_list.append(redemption)
        redemption_id_counter += 1

coupon_redemptions = pd.DataFrame(redemptions_list)
coupon_redemptions.to_csv('data/coupon_redemptions.csv', index=False)
print(f"✓ Created {len(coupon_redemptions)} coupon redemptions")

# 8. Generate MESSY site_visits.csv
print("\n8. Generating site_visits.csv (with data quality issues)...")

num_visits = 75000
visits_list = []

# Use actual customer IDs from orders
customers_by_company = orders.groupby('company_id')['customer_id'].unique().to_dict()

for i in range(num_visits):
    # Pick a random company
    company_id = random.choice(company_ids)
    
    # Random timestamp in last 18 months
    visit_date = datetime.now() - timedelta(days=random.randint(0, 540))
    
    # DATA QUALITY ISSUES:
    
    # 1. Timestamp format issues
    if i % 15 == 0:
        timestamp = visit_date.strftime('%m/%d/%Y %H:%M')  # US format
    elif i % 15 == 1:
        timestamp = visit_date.strftime('%d-%m-%Y %H:%M')  # EU format  
    elif i % 15 == 2:
        timestamp = str(int(visit_date.timestamp()))  # Unix timestamp
    elif i % 50 == 0:
        timestamp = 'INVALID_DATE'
    elif i % 100 == 0:
        timestamp = None
    else:
        timestamp = visit_date.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Customer ID issues
    if company_id in customers_by_company and len(customers_by_company[company_id]) > 0:
        if i % 25 == 0:
            customer_id = None  # Not logged in
        elif i % 40 == 0:
            customer_id = 'invalid_' + str(random.randint(1, 999))
        elif i % 35 == 0:
            customer_id = random.choice(customers_by_company[company_id]).lower()  # Case issue
        elif i % 30 == 0:
            customer_id = random.choice(customers_by_company[company_id]) + ' '  # Trailing space
        else:
            customer_id = random.choice(customers_by_company[company_id]) if random.random() < 0.6 else None
    else:
        customer_id = None
    
    # 3. Company ID issues
    if i % 50 == 0:
        company_id = None  # Missing
    elif i % 60 == 0:
        company_id = company_id.lower()  # Case issue
    elif i % 70 == 0:
        company_id = 'INVALID_COMP'
    
    # 4. Pages viewed - with outliers
    if i % 100 == 0:
        pages_viewed = random.randint(100, 500)  # Bot behavior
    elif i % 80 == 0:
        pages_viewed = 0
    elif i % 75 == 0:
        pages_viewed = -1
    elif i % 60 == 0:
        pages_viewed = None
    elif i % 55 == 0:
        pages_viewed = 'N/A'
    else:
        pages_viewed = np.random.poisson(4) + 1
    
    # 5. Session duration
    if i % 90 == 0:
        session_duration = random.randint(10000, 36000)
    elif i % 85 == 0:
        session_duration = 0
    elif i % 70 == 0:
        session_duration = -random.randint(1, 100)
    elif i % 65 == 0:
        session_duration = None
    elif i % 50 == 0:
        session_duration = 'error'
    else:
        session_duration = int(np.random.exponential(180))
    
    # 6. Traffic source - inconsistent
    sources = ['direct', 'Direct', 'DIRECT', 'direct ', 'email', 'Email', 'EMAIL', 
               'organic', 'Organic', 'google', 'Google', 'facebook', 'Facebook',
               'FB', 'instagram', 'Instagram', 'IG', 'mail', 'direct_mail', 
               'Direct Mail', 'DM', 'catalog', None, 'N/A', 'unknown', '']
    traffic_source = random.choice(sources)
    
    # 7. Conversion flag
    if i % 20 == 0:
        converted = None
    elif i % 30 == 0:
        converted = 'Yes'
    elif i % 35 == 0:
        converted = 'TRUE'
    else:
        converted = 1 if random.random() < 0.025 else 0
    
    # 8. Device type
    devices = ['mobile', 'Mobile', 'MOBILE', 'mob', 'smartphone', 'desktop', 'Desktop', 
              'DESKTOP', 'PC', 'computer', 'tablet', 'Tablet', 'TABLET', 'tab', 'ipad',
              None, 'unknown', 'Unknown', 'N/A']
    device_type = random.choice(devices)
    
    # 9. Session ID - occasional duplicates
    if i % 200 == 0 and i > 0:
        session_id = visits_list[-1]['session_id']
    else:
        session_id = f'S{str(i).zfill(10)}'
    
    visit = {
        'session_id': session_id,
        'customer_id': customer_id,
        'company_id': company_id,
        'visit_timestamp': timestamp,
        'pages_viewed': pages_viewed,
        'session_duration': session_duration,
        'traffic_source': traffic_source,
        'converted': converted,
        'device_type': device_type
    }
    visits_list.append(visit)

# Add complete duplicate rows
for _ in range(500):
    visits_list.append(random.choice(visits_list))

site_visits = pd.DataFrame(visits_list)
site_visits = site_visits.sample(frac=1).reset_index(drop=True)
site_visits.to_csv('data/site_visits.csv', index=False)
print(f"✓ Created {len(site_visits)} site visits (with quality issues)")

# Summary
print("\n" + "=" * 50)
print("✅ All datasets generated successfully!")
print("\nDataset Summary:")
print(f"  • companies.csv: {len(companies)} companies across {len(companies['industry_category'].unique())} industries")
print(f"  • campaigns.csv: {len(campaigns)} campaigns")
print(f"  • postcards.csv: {len(postcards)} postcard sizes")
print(f"  • orders.csv: {len(orders)} treatment group orders")
print(f"  • holdout_orders.csv: {len(holdout_orders)} holdout group records")
print(f"  • coupons.csv: {len(coupons)} coupons")
print(f"  • coupon_redemptions.csv: {len(coupon_redemptions)} redemptions")
print(f"  • site_visits.csv: {len(site_visits)} visits (messy)")

print("\n📊 Key Features:")
print("  • Industry-specific response rates and AOV")
print("  • Holdout groups for incrementality testing (iROAS)")
print("  • Postcard size cost variations")
print("  • A/B test variants with lift")
print("  • Realistic order attribution delays")
print("  • Data quality issues in site_visits for cleaning exercise")

print("\n🎯 Ready for assessment!")
