# Salesforce Flow Blueprint: Onboarding Orchestration Engine

This document outlines the node-by-node configuration for the Record-Triggered Flow in Salesforce Flow Builder.

---

## 1. Flow Metadata
- **Flow Type:** Record-Triggered Flow
- **Object:** `Onboarding_Request__c`
- **Trigger:** A record is created or updated
- **Optimize the Flow for:** Actions and Related Records

---

## 2. Step-by-Step Flow Elements

### Element 1: Start Trigger
- **Condition Requirements:** `None` (Run every time a request is created).

### Element 2: Decision Node — `Evaluate Client Tier & Value`
- **Outcome 1: `Is_Tier_1_Enterprise`**
  - Logic: `Record.MRR__c >= 50000`
- **Outcome 2: `Is_Tier_2_MidMarket`**
  - Logic: `Record.MRR__c >= 10000 AND Record.MRR__c < 50000`
- **Default Outcome: `Is_Tier_3_Growth`**
  - Logic: All other records (`Record.MRR__c < 10000`)

---

### Branch A: Tier 1 (Enterprise) Path

1. **Assignment Element: `Set Tier 1 Attributes`**
   - `{!$Record.Client_Tier__c}` Equals `"Tier 1 - Enterprise"`
   - `{!$Record.Status__c}` Equals `"Security Review"`
   - `{!$Record.SLA_Target_Date__c}` Equals `{!$Flow.CurrentDateTime} + 1` (24 Hours)

2. **Action Element: `Create High-Priority Kickoff Task`**
   - Object: `Task`
   - Subject: `"URGENT: Executive Onboarding Kickoff for " + {!$Record.Account__r.Name}`
   - Priority: `High`
   - DueDate: `{!$Flow.CurrentDate} + 1`
   - WhatId: `{!$Record.Id}`

3. **Post to Chatter / Slack Notification:**
   - Channel: `#enterprise-onboarding-alerts`
   - Message: `"🎉 New Tier 1 Enterprise Deal Won! Account: {!$Record.Account__r.Name} | MRR: ${!$Record.MRR__c}. 24-hr SLA active."`

---

### Branch B: Tier 2 (Mid-Market) Path

1. **Assignment Element: `Set Tier 2 Attributes`**
   - `{!$Record.Client_Tier__c}` Equals `"Tier 2 - Mid-Market"`
   - `{!$Record.Status__c}` Equals `"Assigned"`
   - `{!$Record.SLA_Target_Date__c}` Equals `{!$Flow.CurrentDateTime} + 3` (72 Hours)

2. **Action Element: `Create Standard Implementation Task`**
   - Object: `Task`
   - Subject: `"Send Implementation Setup Packet"`
   - Priority: `Normal`
   - DueDate: `{!$Flow.CurrentDate} + 2`
   - WhatId: `{!$Record.Id}`

---

### Branch C: Tier 3 (Growth) Path

1. **Assignment Element: `Set Tier 3 Attributes`**
   - `{!$Record.Client_Tier__c}` Equals `"Tier 3 - Growth"`
   - `{!$Record.Status__c}` Equals `"Completed"`

2. **Action Element: `Send Automated Welcome Email`**
   - Template: `Self_Service_Welcome_Email`
   - Recipient: `{!$Record.Primary_Contact__r.Email}`

---

## 3. Scheduled Path: SLA Watchdog (24 Hours After CreatedDate)

- **Time Source:** `Record.CreatedDate + 24 Hours`
- **Decision:** `Has Specialist Accepted?`
  - Condition: `{!$Record.Assigned_Specialist__c} IS NULL AND {!$Record.Status__c} != 'Completed'`
- **Action If True (Breach):**
  - Update Records: Set `{!$Record.SLA_Breached__c}` to `TRUE`
  - Set `{!$Record.Status__c}` to `"Escalated"`
  - Send Custom Notification to `Customer Success Director Queue`
