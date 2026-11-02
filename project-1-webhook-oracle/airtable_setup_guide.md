# Airtable Relational Setup Guide: Cold Chain Telemetry Oracle

This guide explains how to set up the Airtable database schema and views for the Webhook Oracle.

---

## 1. Table 1: `Sensor Readings` (Clean Records)

Create a table called **`Sensor Readings`** with the following fields:

| Field Name | Field Type | Details / Format |
| :--- | :--- | :--- |
| `Event ID` | Single line text | Primary field. Holds UUIDv4 |
| `Facility ID` | Single line text | e.g. `FAC-104` |
| `Reading Timestamp` | Date | Include time, ISO format (GMT) |
| `Temperature (°C)` | Number | Decimal (1.0), precision 2 |
| `Humidity (%)` | Number | Integer or Decimal |
| `Sensor Status` | Single select | Options: `ONLINE` (Green), `CALIBRATING` (Yellow), `DEGRADED` (Red) |
| `Ingested At` | Created time | Automated system timestamp |

---

## 2. Table 2: `Anomaly Log` (Quarantine)

Create a second table in the same base called **`Anomaly Log`**:

| Field Name | Field Type | Details / Format |
| :--- | :--- | :--- |
| `Incident ID` | Auto number | Primary field |
| `Event ID` | Single line text | Incoming event ID |
| `Facility ID` | Single line text | Source facility |
| `Reported Temp` | Number | Decimal |
| `Rejection Reason` | Long text | e.g., "Temperature 34.8°C exceeded ceiling limit of 15°C" |
| `Raw Payload` | Long text | Full JSON string for forensic audit |
| `Status` | Single select | `Open` (Red), `Investigating` (Orange), `Resolved` (Green) |
| `Assigned Engineer`| User or Collaborator | Assigned on-call specialist |

---

## 3. Recommended Views in Airtable

1. **Grid View: All Telemetry**: Default view sorted by `Reading Timestamp` descending.
2. **Kanban View: Incidents by Status**: Grouped by `Anomaly Log > Status` to showcase triage workflows.
3. **Gallery View: Facility Summary**: Showing average temperature cards per facility.

---

## 4. Connecting Make.com to Airtable

1. In Make.com, add the **Airtable > Create a Record** module.
2. Connect your Airtable account using a Personal Access Token with scopes: `data.records:write`, `schema.bases:read`.
3. Map the webhook variables:
   - `Event ID` ➔ `{{1.event_id}}`
   - `Facility ID` ➔ `{{1.facility_id}}`
   - `Reading Timestamp` ➔ `{{1.reading_timestamp}}`
   - `Temperature (°C)` ➔ `{{1.temperature_c}}`
   - `Humidity (%)` ➔ `{{1.humidity_pct}}`
   - `Sensor Status` ➔ `{{1.sensor_status}}`
