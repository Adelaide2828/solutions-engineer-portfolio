# Data Dictionary: Enterprise Onboarding Request

**Object API Name:** `Onboarding_Request__c`  
**Object Label:** Onboarding Request  
**Plural Label:** Onboarding Requests  
**Sharing Model:** Read/Write (Controlled by Parent: Account)

---

## Field Specifications

| Field Label | API Name | Data Type | Length / Details | Required? | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Request Number** | `Name` | Auto-Number | `ONB-{0000}` | Yes | System generated reference number. |
| **Account** | `Account__c` | Master-Detail | Master: Account | Yes | The parent company initiating onboarding. |
| **Primary Contact** | `Primary_Contact__c` | Lookup | Lookup: Contact | Yes | The primary technical or business stakeholder. |
| **Monthly Recurring Revenue** | `MRR__c` | Currency | 16, 2 | Yes | Contractual monthly revenue for SLA weighting. |
| **Client Tier** | `Client_Tier__c` | Picklist | `Tier 1 - Enterprise`<br>`Tier 2 - Mid-Market`<br>`Tier 3 - Growth` | Yes | Calculated automatically by Flow or formula. |
| **Status** | `Status__c` | Picklist | `New`<br>`Assigned`<br>`Security Review`<br>`In Progress`<br>`Completed`<br>`Escalated` | Yes | Lifecycle phase of the onboarding journey. |
| **Assigned Specialist** | `Assigned_Specialist__c`| Lookup | Lookup: User | No | Assigned Solutions Architect or Implementation lead. |
| **SLA Target Due Date** | `SLA_Target_Date__c` | Date/Time | — | No | Target first-touch milestone (Calculated: CreatedDate + 24 hours). |
| **SLA Breached** | `SLA_Breached__c` | Checkbox | Default: False | No | Flag set by scheduled flow if first touch missed. |
| **Security Clearance Required** | `Security_Clearance__c`| Checkbox | Default: False | No | Indicates SOC2 / HIPAA / ISO compliance review needed. |
| **Kickoff Notes** | `Kickoff_Notes__c` | Long Text Area | 32,768 chars | No | Implementation scoping notes and tech stack details. |

---

## Validation Rules

### 1. `Require_Security_Clearance_For_Tier1`
- **Error Condition Formula:**
  ```text
  AND(
      ISPICKVAL(Client_Tier__c, "Tier 1 - Enterprise"),
      ISBLANK(TEXT(Security_Clearance__c))
  )
  ```
- **Error Message:** *"All Tier 1 Enterprise accounts must explicitly specify whether Security Clearance is required before saving."*

### 2. `Cannot_Complete_Without_Specialist`
- **Error Condition Formula:**
  ```text
  AND(
      ISPICKVAL(Status__c, "Completed"),
      ISBLANK(Assigned_Specialist__c)
  )
  ```
- **Error Message:** *"An onboarding request cannot be marked as Completed without an assigned implementation specialist."*
