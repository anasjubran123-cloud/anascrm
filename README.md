# Personal CRM Cockpit (Single-User, Offline-First)

A local-first personal CRM for a sales/account/BD lead in a systems integrator context (DC/AV/IT/Events/Low Current).

## What this build includes

- Relational SQLite data model with foreign keys for core CRM entities.
- Unified Opportunity + Tender lifecycle handling.
- Interaction timeline separated from system Activity Log.
- Stage gates + probability automation + status outcome rules.
- Tasking + reminders + stalled opportunity automation.
- Vendor/partner management and opportunity linkage.
- Versioned quotes + quote line items schema.
- Tender checklist/clarification schema.
- Offline-first integrations using reference links only (email/calendar/doc links).
- Duplicate detection suggestions.
- Dashboard with pipeline/forecast/activities.
- CSV export.
- Encrypted backup + restore with rotating retention.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes on architecture

- `personal_crm.db` is the source of truth.
- External systems are referenced via deep links/IDs only.
- If an external email/event link breaks, CRM record remains intact.
- Stage/probability map is configurable in code and manual override is preserved.

## Core files

- `app.py`: app UI, schema bootstrap, automations, and backup logic.
- `requirements.txt`: dependencies.
