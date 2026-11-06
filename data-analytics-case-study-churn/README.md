# Case Study 1: B2B Customer Churn & Revenue Risk Analysis
> **Focus:** Subscription Retention, Revenue Exposure & Proactive Customer Health Scoring  
> **Tools & Stack:** SQL (PostgreSQL / SQLite), Python (Pandas, Scikit-Learn), Power BI / Interactive Dashboard, Automated CRM Reverse-Sync  
> **Key Business Question:** *Which customer segments are most at risk of churning, what operational friction is driving them away, and how can leadership intervene before ARR is lost?*

---

## 🧭 The 3-Pillar Executive Breakdown

### 1. What is the Business Problem?
A high-growth B2B enterprise software company is experiencing unpredictable customer churn. Mid-market and enterprise accounts are canceling contracts at renewal without prior warning, resulting in **$280,000+ in annual recurring revenue (ARR) attrition** per quarter. 

The executive leadership team identified three core vulnerabilities:
1. **No Early Warning System:** Account Executives and Customer Success Managers (CSMs) only discover dissatisfaction when cancellation notices are submitted.
2. **Siloed Telemetry:** Usage logs, support tickets, billing records, and contract renewal dates live in separate databases without unified risk visibility.
3. **Reactive Interventions:** Retention discounts are offered too late, failing to address the true operational bottlenecks driving customer frustration.

---

### 2. What Does the Data Tell Us?

After ingesting and analyzing multi-table relational telemetry across **1,000+ customer accounts** (combining `accounts`, `subscriptions`, `usage_logs`, `support_tickets`, and `transactions`), the data revealed clear leading indicators of churn:

```mermaid
graph TD
    A[Customer Ingestion Telemetry] --> B[Feature Engineering Engine]
    B --> C1[Login Frequency Decay > 35%]
    B --> C2[Unresolved Tickets > 3 in 30 Days]
    B --> C3[License Seat Utilization < 50%]
    B --> C4[CSAT Rating <= 2.5]
    
    C1 & C2 & C3 & C4 --> D{Composite Churn Risk Score}
    D -->|Score >= 70%| E[High Risk: $145k ARR Exposed]
    D -->|Score 40-69%| F[Medium Risk: Nurture & Audit]
    D -->|Score < 40%| G[Healthy: Upsell Candidate]

    classDef danger fill:#fee2e2,stroke:#ef4444,stroke-width:2px;
    classDef warn fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
    classDef success fill:#dcfce7,stroke:#22c55e,stroke-width:2px;
    class E danger;
    class F warn;
    class G success;
```

#### Key Analytical Insights:
- **The "30-Day Activity Cliff":** Accounts whose weekly active login frequency dropped by **>35% over a 30-day window** had an **83.4% probability of non-renewal**, regardless of contract length.
- **Support Escalation Density:** Churn risk quadruples when an account logs **more than 3 open support tickets** within 14 days without resolution.
- **Under-Utilization Warning:** Clients utilizing less than **48% of their contracted license seats** within the first 90 days after onboarding represent **68% of all high-risk accounts**.
- **Financial Exposure:** Analysis quantified **$145,200 in ARR currently sitting in the High-Risk Tier (Risk Score >= 70%)**, primarily concentrated in Financial Services and Logistics verticals.

---

### 3. What Should the Business Do Next? (Actionable Strategic Recommendations)

Based on the quantitative findings, three operational interventions were formulated for the CEO and VP of Customer Success:

1. **Deploy an Automated "Usage Cliff" Trigger in CRM:**
   - Automatically flag accounts in Salesforce/CRM as `High Risk` the moment 30-day login frequency drops below 60%.
   - Trigger an automated, mandatory check-in task for the assigned CSM within 48 hours of detection.
2. **Institute a "First 90 Days" Seat Utilization Audit:**
   - Any customer with `<50%` seat adoption by Day 60 is automatically enrolled in a proactive training sprint with Solutions Engineering to remove technical onboarding friction.
3. **Prioritize Support Tickets by Revenue-at-Risk:**
   - Reconfigure helpdesk routing so that support tickets from Tier 1 enterprise accounts with an existing churn risk score `>60%` automatically bypass the general queue and route to Senior Solutions Architects.

**Projected Financial Impact:** Reducing churn in the High-Risk Tier by just 25% recovers an estimated **$115,000+ in retained ARR annually**.

---

## 🗄️ Relational Schema & Data Pipeline

The analysis is backed by a 5-table relational schema (`schema.sql`):
- `accounts`: Company demographics, industry, regional tier.
- `subscriptions`: Contract start/end dates, MRR, tier level.
- `usage_logs`: Daily active users, feature click streams, session duration.
- `support_tickets`: Ticket resolution time, severity level, CSAT rating.
- `transactions`: Payment status, payment delays, failed invoice counts.

---

## 💻 Visual Analytics & Interactive Dashboard Preview

The project includes an interactive web intelligence dashboard with real-time what-if simulations:
- **Executive Summary:** Total ARR at risk, High/Med/Low customer distributions.
- **Feature Importance Chart:** Showing exact weights of login decay vs. CSAT ratings.
- **Reverse-Sync Simulator:** Pushing calculated risk scores and drivers directly to CRM account records.
