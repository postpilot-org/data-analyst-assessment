
-- SQL Setup Instructions for Exercises 1 & 2
-- =============================================
-- You can use any SQL database. Here are options:

-- Option 1: SQLite (Simplest)
-- ---------------------------
-- Use SQLite command line or a tool like DB Browser for SQLite
-- Import CSV files directly using the import wizard

-- Option 2: PostgreSQL
-- --------------------
-- Create database and tables, then import CSVs:

CREATE DATABASE marketing_assessment;
\c marketing_assessment;

-- Create tables
CREATE TABLE companies (
    company_id VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(200),
    industry_category VARCHAR(100),
    signup_date DATE,
    monthly_budget DECIMAL(10,2)
);

CREATE TABLE postcards (
    id VARCHAR(10) PRIMARY KEY,
    size VARCHAR(20),
    cost_per_piece DECIMAL(10,2)
);

CREATE TABLE campaigns (
    campaign_id VARCHAR(10) PRIMARY KEY,
    company_id VARCHAR(10),
    campaign_name VARCHAR(200),
    mail_drop_date DATE,
    postcard_size VARCHAR(10),
    quantity_sent INTEGER,
    holdout_size INTEGER,
    campaign_type VARCHAR(50),
    test_group VARCHAR(50)
);

CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    company_id VARCHAR(10),
    customer_id VARCHAR(30),
    order_date TIMESTAMP,
    order_amount DECIMAL(10,2),
    attribution_campaign_id VARCHAR(10),
    attribution_type VARCHAR(50),
    days_from_mail_drop INTEGER
);

CREATE TABLE holdout_orders (
    company_id VARCHAR(10),
    campaign_id VARCHAR(10),
    holdout_period_start DATE,
    holdout_period_end DATE,
    total_customers INTEGER,
    total_orders INTEGER,
    total_revenue DECIMAL(10,2)
);

CREATE TABLE coupons (
    coupon_code VARCHAR(50) PRIMARY KEY,
    coupon_name VARCHAR(200),
    discount_type VARCHAR(50),
    discount_value DECIMAL(10,2),
    usage_type VARCHAR(50),
    max_uses INTEGER,
    min_purchase_amount DECIMAL(10,2),
    valid_from DATE,
    valid_until DATE,
    campaign_id VARCHAR(10)
);

CREATE TABLE coupon_redemptions (
    redemption_id VARCHAR(20) PRIMARY KEY,
    coupon_code VARCHAR(50),
    order_id VARCHAR(20),
    customer_id VARCHAR(30),
    redemption_date TIMESTAMP,
    discount_applied DECIMAL(10,2)
);

-- Import CSVs (PostgreSQL)
\copy companies FROM 'data/companies.csv' WITH CSV HEADER;
\copy postcards FROM 'data/postcards.csv' WITH CSV HEADER;
\copy campaigns FROM 'data/campaigns.csv' WITH CSV HEADER;
\copy orders FROM 'data/orders.csv' WITH CSV HEADER;
\copy holdout_orders FROM 'data/holdout_orders.csv' WITH CSV HEADER;
\copy coupons FROM 'data/coupons.csv' WITH CSV HEADER;
\copy coupon_redemptions FROM 'data/coupon_redemptions.csv' WITH CSV HEADER;

-- Option 3: MySQL
-- ---------------
-- Similar to PostgreSQL, adjust data types as needed:
-- VARCHAR -> VARCHAR
-- DECIMAL -> DECIMAL  
-- BOOLEAN -> TINYINT(1)

-- Option 4: DuckDB (Great for analytical queries)
-- ------------------------------------------------
-- Install DuckDB and run:
/*
CREATE TABLE companies AS SELECT * FROM read_csv_auto('data/companies.csv');
CREATE TABLE postcards AS SELECT * FROM read_csv_auto('data/postcards.csv');
CREATE TABLE campaigns AS SELECT * FROM read_csv_auto('data/campaigns.csv');
CREATE TABLE orders AS SELECT * FROM read_csv_auto('data/orders.csv');
CREATE TABLE holdout_orders AS SELECT * FROM read_csv_auto('data/holdout_orders.csv');
CREATE TABLE coupons AS SELECT * FROM read_csv_auto('data/coupons.csv');
CREATE TABLE coupon_redemptions AS SELECT * FROM read_csv_auto('data/coupon_redemptions.csv');
*/

-- Option 5: Google BigQuery (if you prefer cloud)
-- ------------------------------------------------
-- Upload CSVs to BigQuery using the web console
-- Auto-detect schema should work for these files

-- =============================================
-- Quick Data Validation Queries
-- =============================================

-- Check row counts
SELECT 'companies' as table_name, COUNT(*) as row_count FROM companies
UNION ALL
SELECT 'postcards', COUNT(*) FROM postcards
UNION ALL
SELECT 'campaigns', COUNT(*) FROM campaigns
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'holdout_orders', COUNT(*) FROM holdout_orders
UNION ALL
SELECT 'coupons', COUNT(*) FROM coupons
UNION ALL
SELECT 'coupon_redemptions', COUNT(*) FROM coupon_redemptions;

-- Verify campaign costs can be calculated
SELECT 
    c.campaign_id,
    c.quantity_sent,
    c.postcard_size,
    p.cost_per_piece,
    (c.quantity_sent * p.cost_per_piece) as total_campaign_cost
FROM campaigns c
JOIN postcards p ON c.postcard_size = p.id
LIMIT 5;

-- Check ROAS calculation components
SELECT 
    c.campaign_id,
    c.quantity_sent * p.cost_per_piece as campaign_cost,
    COUNT(o.order_id) as order_count,
    SUM(o.order_amount) as total_revenue,
    SUM(o.order_amount) / (c.quantity_sent * p.cost_per_piece) as ROAS
FROM campaigns c
JOIN postcards p ON c.postcard_size = p.id
LEFT JOIN orders o ON c.campaign_id = o.attribution_campaign_id
GROUP BY c.campaign_id, c.quantity_sent, p.cost_per_piece
LIMIT 5;
