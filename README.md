# Data Analyst Technical Assessment

## Company Context
We are a direct mail marketing company integrated with Shopify. We send physical mail campaigns with promotional codes and track their performance through our digital attribution system. We work with clients across various industries and need to understand performance benchmarks and optimization opportunities.

**Time Limit:** 3 hours  
**Submission:** Fork this repository, complete both questions, and submit a pull request.

> **Note:** All required data files are already included in the `data/` directory. You do not need to generate any data. The `generate_datasets.py` file is for internal use only.

## Repository Structure
```
data-analyst-assessment/
│
├── README.md                           # This file
├── data/
│   ├── companies.csv                  # Client company information
│   ├── campaigns.csv                  # Campaign information
│   ├── orders.csv                     # Order/transaction data
│   ├── holdout_orders.csv             # Holdout group performance
│   ├── postcards.csv                  # Postcard specifications and costs
│   ├── coupons.csv                    # Coupon metadata
│   ├── coupon_redemptions.csv         # Actual coupon usage
│   └── site_visits.csv                # Website tracking data
├── question_1/
│   ├── part_a_benchmarks.sql          # Your benchmark calculations
│   ├── part_b_dashboard.sql           # Your dashboard queries
│   ├── dashboard_output/               # Your visualization files
│   └── analysis_summary.md            # Your findings and recommendations
├── question_2/
│   ├── data_quality_analysis.ipynb    # Your Python solution
│   └── cleaned_site_visits.csv        # Your cleaned output
└── requirements.txt                    # Python dependencies
```

---

## Question 1: Campaign Performance Analysis

A major client is requesting a comprehensive performance review. They want to understand how their campaigns compare to industry benchmarks and need a dashboard to track ongoing performance.

### Part A: Calculate Industry Benchmarks

**Task:** Write SQL queries to calculate ROAS and iROAS benchmarks by industry. Consider what statistical measures would be most useful for setting realistic client expectations.

**Deliverable:** SQL queries in `part_a_benchmarks.sql`

### Part B: Campaign Performance Dashboard & Strategic Insights

**Task:** The client wants:
1. A dashboard visualizing their current campaign performance against the industry benchmarks you calculated
2. Analysis of which coupon types perform best
3. Segment analysis identifying which customer segments and campaign types we should invest more in

Create the SQL queries to power this dashboard and produce visualizations showing:
- Current campaign ROAS/iROAS vs. industry benchmarks
- Coupon performance by type
- Segment profitability analysis with expansion recommendations
- A/B test results if applicable

**Deliverables:** 
- SQL queries in `part_b_dashboard.sql`
- At least 4 visualizations in `dashboard_output/` (use any tool: Python, Tableau, Excel, etc.)
- Summary with strategic recommendations in `analysis_summary.md`

---

## Question 2: Data Quality Assessment

### Context
Our Data Science team wants to use the `site_visits.csv` data for predictive modeling but needs it cleaned first.

### Task
Use Python to:
1. Identify and document all data quality issues
2. Clean the dataset appropriately
3. Provide recommendations for data collection improvements

### Deliverables
- Jupyter notebook with your analysis (`data_quality_analysis.ipynb`)
- Cleaned dataset (`cleaned_site_visits.csv`)

---

## Dataset Descriptions

### companies.csv
- `company_id`: Unique client identifier
- `company_name`: Client company name
- `industry_category`: Shopify industry classification
- `signup_date`: When they became a client
- `monthly_budget`: Average monthly spend with us

### campaigns.csv
- `campaign_id`: Unique campaign identifier
- `company_id`: Client who ran the campaign
- `campaign_name`: Name of the campaign
- `mail_drop_date`: Date mail was sent
- `postcard_size`: Size used (matches postcards.id)
- `quantity_sent`: Number of pieces mailed
- `holdout_size`: Number of customers in holdout group
- `campaign_type`: Purpose (acquisition, retention, winback, seasonal)
- `test_group`: A/B test variant (control, variant_a, variant_b)

### postcards.csv
- `id`: Postcard size identifier
- `size`: Dimensions (e.g., "4x6", "5x7", "6x9", "6x11")
- `cost_per_piece`: Production and postage cost per unit

### orders.csv
- `order_id`: Unique order identifier
- `company_id`: Which client's customer made the order
- `customer_id`: Customer who placed the order
- `order_date`: Purchase date
- `order_amount`: Total order value
- `attribution_campaign_id`: Campaign that drove the order
- `attribution_type`: How attribution was determined
- `days_from_mail_drop`: Days between mail delivery and order

### holdout_orders.csv
- `company_id`: Client company
- `campaign_id`: Associated campaign
- `holdout_period_start`: Start of measurement window
- `holdout_period_end`: End of measurement window
- `total_customers`: Number of customers in holdout
- `total_orders`: Orders from holdout group
- `total_revenue`: Revenue from holdout group

### coupons.csv
- `coupon_code`: Unique coupon identifier
- `coupon_name`: Display name
- `discount_type`: percentage, fixed_amount, free_shipping, bogo
- `discount_value`: Amount or percentage
- `usage_type`: single_use, multi_use, static
- `max_uses`: Maximum redemptions allowed
- `min_purchase_amount`: Minimum order for eligibility
- `valid_from`: Start date
- `valid_until`: Expiration date
- `campaign_id`: Associated campaign

### coupon_redemptions.csv
- `redemption_id`: Unique redemption identifier
- `coupon_code`: Coupon that was used
- `order_id`: Associated order
- `customer_id`: Who redeemed it
- `redemption_date`: When it was used
- `discount_applied`: Actual discount amount given

### site_visits.csv
- `session_id`: Unique session identifier
- `customer_id`: Customer identifier (if known)
- `company_id`: Which client's site was visited
- `visit_timestamp`: When the visit occurred
- `pages_viewed`: Number of pages in session
- `session_duration`: Time spent on site
- `traffic_source`: How they arrived
- `converted`: Whether they made a purchase
- `device_type`: Device used

---

## Evaluation Criteria

We will evaluate submissions based on:

1. **Technical Proficiency** - SQL and Python code quality, efficiency
2. **Analytical Thinking** - Approach to benchmarking and segmentation
3. **Business Acumen** - Understanding of marketing metrics and strategic recommendations
4. **Data Visualization** - Clear, insightful visual communication
5. **Attention to Detail** - Thoroughness in data quality assessment

---

## Setup Instructions

```bash
# Clone the repository
git clone [repository-url]
cd data-analyst-assessment

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Verify setup
python check_setup.py

# Start Jupyter for Python work
jupyter notebook
```

## Submission Guidelines

1. Fork this repository
2. Complete both questions with all parts
3. Ensure SQL files are properly formatted and commented
4. Include clear visualizations with appropriate labels
5. Document your analytical approach and decisions
6. Submit a pull request with your solutions

---

*Note: Focus on demonstrating your analytical process, business thinking, and ability to derive actionable insights from data.*
