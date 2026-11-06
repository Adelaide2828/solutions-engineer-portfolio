-- Revenue Pipeline & Churn Prediction Engine Schema
-- SQL DDL for Multi-Table Enterprise B2B SaaS Relational Data

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS usage_logs;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS accounts;

-- Accounts Table: Enterprise customer profiles
CREATE TABLE accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    company_size VARCHAR(20) NOT NULL, -- e.g. SMB, Mid-Market, Enterprise
    created_at TIMESTAMP NOT NULL,
    country VARCHAR(50) DEFAULT 'USA',
    primary_contact_email VARCHAR(100)
);

-- Subscriptions Table: Active & historical contract details
CREATE TABLE subscriptions (
    subscription_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    plan_tier VARCHAR(30) NOT NULL, -- Starter, Pro, Enterprise
    contract_type VARCHAR(20) NOT NULL, -- Monthly, Annual
    mrr DECIMAL(10, 2) NOT NULL,
    licensed_seats INT NOT NULL,
    active_seats INT NOT NULL,
    start_date DATE NOT NULL,
    renewal_date DATE NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Usage Logs Table: High-frequency operational telemetry
CREATE TABLE usage_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id VARCHAR(50) NOT NULL,
    log_date DATE NOT NULL,
    login_count INT DEFAULT 0,
    api_calls_count INT DEFAULT 0,
    feature_a_usage INT DEFAULT 0, -- Core Workflow
    feature_b_usage INT DEFAULT 0, -- Analytics Export
    feature_c_usage INT DEFAULT 0, -- Integrations
    active_users_count INT DEFAULT 0,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Support Tickets Table: Customer service & satisfaction records
CREATE TABLE support_tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    priority VARCHAR(20) NOT NULL, -- Low, Medium, High, Urgent
    status VARCHAR(20) NOT NULL, -- Open, In Progress, Resolved
    category VARCHAR(50), -- Billing, Technical, Bug, Feature Request
    csat_score INT, -- 1 to 5 scale
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Transactions Table: Billing, invoices, and payment tracking
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_date DATE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL, -- Paid, Late, Pending, Failed
    payment_delay_days INT DEFAULT 0,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
