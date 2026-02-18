import base64
import hashlib
import json
import os
import shutil
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
from cryptography.fernet import Fernet

DB_PATH = Path("personal_crm.db")
BACKUP_DIR = Path("backups")

OPEN_STAGES = [
    "Identified",
    "Lead",
    "Qualified",
    "Presales Design",
    "Proposal & Quote",
    "Negotiation",
    "On Hold",
]
STAGE_PROBABILITY = {
    "Identified": 10,
    "Lead": 20,
    "Qualified": 30,
    "Presales Design": 45,
    "Proposal & Quote": 60,
    "Negotiation": 80,
    "On Hold": 20,
}
LOSS_REASONS = [
    "Price",
    "Technical mismatch",
    "Commercial terms",
    "Client cancelled",
    "Competitor relationship",
    "Other",
]
NO_PARTICIPATION_REASONS = [
    "Scope mismatch",
    "Capacity constraints",
    "Commercial risk",
    "Documentation not ready",
    "Other",
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def normalize_email(value: str):
    return value.strip().lower() if value else None


def normalize_phone(value: str):
    if not value:
        return None
    digits = "".join(ch for ch in value if ch.isdigit() or ch == "+")
    return digits or value.strip()


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def activity_log(conn, linked_entity, linked_id, activity_type, description):
    conn.execute(
        """
        INSERT INTO activity_log(linked_entity,linked_id,date_time,activity_type,description)
        VALUES(?,?,?,?,?)
        """,
        (linked_entity, linked_id, now_iso(), activity_type, description),
    )


def init_db():
    with closing(get_conn()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );

            CREATE TABLE IF NOT EXISTS client_group (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                client_group_id INTEGER,
                sector TEXT,
                region TEXT,
                account_priority TEXT,
                division_focus TEXT,
                status TEXT,
                primary_contact_id INTEGER,
                notes TEXT,
                FOREIGN KEY(client_group_id) REFERENCES client_group(id),
                FOREIGN KEY(primary_contact_id) REFERENCES contact(id)
            );

            CREATE TABLE IF NOT EXISTS site (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                city_region TEXT,
                address TEXT,
                notes TEXT,
                FOREIGN KEY(client_id) REFERENCES client(id)
            );

            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                site_id INTEGER,
                name TEXT NOT NULL,
                job_title TEXT,
                role TEXT,
                email TEXT,
                phone TEXT,
                preferred_channel TEXT,
                notes TEXT,
                FOREIGN KEY(client_id) REFERENCES client(id),
                FOREIGN KEY(site_id) REFERENCES site(id)
            );

            CREATE TABLE IF NOT EXISTS vendor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT,
                partner_tier TEXT,
                territory_region TEXT,
                product_lines TEXT,
                notes TEXT,
                main_account_manager_name TEXT,
                main_account_manager_email TEXT,
                main_account_manager_phone TEXT,
                main_technical_contacts TEXT,
                default_vendor_payment_terms TEXT,
                deal_registration_possible INTEGER,
                deal_registration_status TEXT,
                deal_registration_id TEXT,
                deal_registration_expiry_date TEXT,
                nda_status TEXT,
                nda_expiry_date TEXT,
                escalation_support_notes TEXT,
                typical_lead_time_days INTEGER
            );

            CREATE TABLE IF NOT EXISTS tender (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reference_number TEXT UNIQUE,
                issuing_client_id INTEGER NOT NULL,
                linked_opportunity_id INTEGER,
                divisions TEXT,
                role TEXT,
                prime_company_name TEXT,
                consultant TEXT,
                announcement_date TEXT,
                site_visit_datetime TEXT,
                clarification_deadline TEXT,
                submission_datetime TEXT,
                technical_opening_date TEXT,
                commercial_opening_date TEXT,
                bid_bond_expiry_date TEXT,
                estimated_tender_value REAL,
                bid_bond_required INTEGER,
                bid_bond_amount REAL,
                pricing_margin_notes TEXT,
                tender_status TEXT,
                result_summary TEXT,
                reason_for_loss_no_participation TEXT,
                notes TEXT,
                action_plan_summary TEXT,
                FOREIGN KEY(issuing_client_id) REFERENCES client(id),
                FOREIGN KEY(linked_opportunity_id) REFERENCES opportunity(id)
            );

            CREATE TABLE IF NOT EXISTS opportunity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                client_id INTEGER NOT NULL,
                site_id INTEGER,
                division TEXT,
                region TEXT,
                account_priority TEXT,
                opportunity_type TEXT,
                source TEXT,
                stage TEXT,
                probability INTEGER,
                probability_manual_override INTEGER DEFAULT 0,
                stage_entered_date TEXT,
                status TEXT,
                reason_for_loss TEXT,
                loss_notes TEXT,
                currency TEXT DEFAULT 'SAR',
                estimated_deal_value REAL DEFAULT 0,
                estimated_cost_equipment REAL DEFAULT 0,
                estimated_cost_services REAL DEFAULT 0,
                estimated_cost_subcontractor REAL DEFAULT 0,
                payment_terms TEXT,
                credit_risk_flags TEXT,
                forecast_category TEXT,
                date_identified TEXT,
                expected_close_date TEXT,
                actual_close_date TEXT,
                last_activity_date TEXT,
                next_action_date TEXT,
                category TEXT,
                linked_tender_id INTEGER,
                competitors TEXT,
                notes TEXT,
                FOREIGN KEY(client_id) REFERENCES client(id),
                FOREIGN KEY(site_id) REFERENCES site(id),
                FOREIGN KEY(linked_tender_id) REFERENCES tender(id)
            );

            CREATE TABLE IF NOT EXISTS opportunity_vendor (
                opportunity_id INTEGER,
                vendor_id INTEGER,
                PRIMARY KEY(opportunity_id, vendor_id),
                FOREIGN KEY(opportunity_id) REFERENCES opportunity(id) ON DELETE CASCADE,
                FOREIGN KEY(vendor_id) REFERENCES vendor(id)
            );

            CREATE TABLE IF NOT EXISTS interaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_time TEXT NOT NULL,
                type TEXT,
                direction TEXT,
                client_id INTEGER NOT NULL,
                linked_contacts TEXT,
                linked_opportunity_id INTEGER,
                linked_tender_id INTEGER,
                summary TEXT,
                detailed_notes TEXT,
                outcome TEXT,
                next_step TEXT,
                next_step_date TEXT,
                email_reference_link TEXT,
                location TEXT,
                FOREIGN KEY(client_id) REFERENCES client(id),
                FOREIGN KEY(linked_opportunity_id) REFERENCES opportunity(id),
                FOREIGN KEY(linked_tender_id) REFERENCES tender(id)
            );

            CREATE TABLE IF NOT EXISTS opportunity_contact_role (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER NOT NULL,
                contact_id INTEGER NOT NULL,
                role_in_deal TEXT,
                influence_score INTEGER,
                relationship_strength INTEGER,
                stance TEXT,
                notes TEXT,
                FOREIGN KEY(opportunity_id) REFERENCES opportunity(id) ON DELETE CASCADE,
                FOREIGN KEY(contact_id) REFERENCES contact(id)
            );

            CREATE TABLE IF NOT EXISTS quote (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER NOT NULL,
                tender_id INTEGER,
                quote_version INTEGER NOT NULL,
                status TEXT,
                currency TEXT,
                vat_percent REAL,
                assumptions_notes TEXT,
                submitted_date TEXT,
                valid_until TEXT,
                FOREIGN KEY(opportunity_id) REFERENCES opportunity(id) ON DELETE CASCADE,
                FOREIGN KEY(tender_id) REFERENCES tender(id)
            );

            CREATE TABLE IF NOT EXISTS quote_line_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote_id INTEGER NOT NULL,
                line_type TEXT,
                vendor_id INTEGER,
                sku_part_number TEXT,
                description TEXT,
                quantity REAL,
                unit_selling_price REAL,
                unit_cost REAL,
                lead_time_days INTEGER,
                notes TEXT,
                FOREIGN KEY(quote_id) REFERENCES quote(id) ON DELETE CASCADE,
                FOREIGN KEY(vendor_id) REFERENCES vendor(id)
            );

            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                linked_to_type TEXT,
                linked_to_id INTEGER,
                due_date TEXT,
                start_date TEXT,
                priority TEXT,
                status TEXT,
                role_related_to TEXT,
                next_follow_up_date TEXT,
                waiting_on TEXT,
                blocked_by_task_id INTEGER,
                reminder TEXT,
                created_at TEXT,
                FOREIGN KEY(blocked_by_task_id) REFERENCES task(id)
            );

            CREATE TABLE IF NOT EXISTS task_update (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                date_time TEXT,
                update_text TEXT,
                outcome TEXT,
                FOREIGN KEY(task_id) REFERENCES task(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS approval_request (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                linked_type TEXT,
                linked_id INTEGER,
                requested_date TEXT,
                requested_from_role TEXT,
                status TEXT,
                decision_date TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS document_link (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                linked_type TEXT,
                linked_id INTEGER,
                display_name TEXT,
                file_or_url TEXT,
                notes TEXT,
                document_type TEXT
            );

            CREATE TABLE IF NOT EXISTS tender_checklist_template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                checklist_category TEXT,
                item_name TEXT,
                required INTEGER,
                owner_role_mode TEXT
            );

            CREATE TABLE IF NOT EXISTS tender_checklist_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tender_id INTEGER NOT NULL,
                checklist_category TEXT,
                item_name TEXT,
                required INTEGER,
                owner_role_mode TEXT,
                due_date TEXT,
                status TEXT,
                linked_document_id INTEGER,
                notes TEXT,
                FOREIGN KEY(tender_id) REFERENCES tender(id) ON DELETE CASCADE,
                FOREIGN KEY(linked_document_id) REFERENCES document_link(id)
            );

            CREATE TABLE IF NOT EXISTS tender_clarification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tender_id INTEGER NOT NULL,
                question TEXT,
                category TEXT,
                submitted_date TEXT,
                response_date TEXT,
                response_summary TEXT,
                impact TEXT,
                linked_documents TEXT,
                notes TEXT,
                FOREIGN KEY(tender_id) REFERENCES tender(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                linked_entity TEXT,
                linked_id INTEGER,
                date_time TEXT,
                activity_type TEXT,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS unmatched_sender (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_email TEXT,
                sender_name TEXT,
                source_ref TEXT,
                summary TEXT,
                created_at TEXT
            );
            """
        )
        conn.commit()


def validate_stage_gate(conn, opportunity_id, new_stage):
    opp = conn.execute("SELECT * FROM opportunity WHERE id=?", (opportunity_id,)).fetchone()
    if not opp:
        return "Opportunity not found"
    if new_stage == "Qualified":
        mandatory = [opp["client_id"], opp["opportunity_type"], opp["estimated_deal_value"], opp["expected_close_date"], opp["next_action_date"]]
        if not all(mandatory):
            return "Qualified gate requires client, type, deal value, expected close, and next action date"
        contact_count = conn.execute(
            "SELECT COUNT(*) c FROM contact WHERE client_id=?", (opp["client_id"],)
        ).fetchone()["c"]
        if contact_count == 0 and not (opp["notes"] and "No contact yet" in opp["notes"]):
            return "Need at least one contact or note 'No contact yet'"
    if new_stage == "Presales Design":
        mapped = conn.execute(
            "SELECT COUNT(*) c FROM opportunity_contact_role WHERE opportunity_id=?", (opportunity_id,)
        ).fetchone()["c"]
        recent_interaction = conn.execute(
            "SELECT COUNT(*) c FROM interaction WHERE linked_opportunity_id=? AND date(date_time) >= date('now','-14 day')",
            (opportunity_id,),
        ).fetchone()["c"]
        if mapped == 0 and recent_interaction == 0:
            return "Need stakeholder mapping or recent interaction in last 14 days"
    if new_stage == "Proposal & Quote":
        quote_count = conn.execute("SELECT COUNT(*) c FROM quote WHERE opportunity_id=?", (opportunity_id,)).fetchone()["c"]
        prep_task = conn.execute(
            "SELECT COUNT(*) c FROM task WHERE linked_to_type='Opportunity' AND linked_to_id=? AND lower(title) like '%prepare quote%'",
            (opportunity_id,),
        ).fetchone()["c"]
        if quote_count == 0 and prep_task == 0:
            return "Need at least one quote or a 'Prepare Quote' task"
    if new_stage == "Negotiation":
        submitted_quote = conn.execute(
            "SELECT COUNT(*) c FROM quote WHERE opportunity_id=? AND status in ('Submitted','Final')", (opportunity_id,)
        ).fetchone()["c"]
        if submitted_quote == 0 and not (opp["notes"] and "negotiation basis" in opp["notes"].lower()):
            return "Need submitted quote or note explaining negotiation basis"
    return None


def update_opportunity_stage(conn, opportunity_id, new_stage):
    gate_error = validate_stage_gate(conn, opportunity_id, new_stage)
    if gate_error:
        return gate_error
    opp = conn.execute("SELECT stage, probability_manual_override FROM opportunity WHERE id=?", (opportunity_id,)).fetchone()
    if not opp:
        return "Opportunity not found"
    new_prob = STAGE_PROBABILITY.get(new_stage, 20)
    if opp["probability_manual_override"]:
        conn.execute(
            "UPDATE opportunity SET stage=?, stage_entered_date=? WHERE id=?",
            (new_stage, date.today().isoformat(), opportunity_id),
        )
    else:
        conn.execute(
            "UPDATE opportunity SET stage=?, probability=?, stage_entered_date=? WHERE id=?",
            (new_stage, new_prob, date.today().isoformat(), opportunity_id),
        )
    activity_log(conn, "Opportunity", opportunity_id, "Stage change", f"{opp['stage']} -> {new_stage}")
    if new_stage == "Proposal & Quote":
        due = (date.today() + timedelta(days=5)).isoformat()
        conn.execute(
            """
            INSERT INTO task(title, description, linked_to_type, linked_to_id, due_date, priority, status, role_related_to, reminder, created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                "Follow-up proposal",
                "Chase client after proposal submission",
                "Opportunity",
                opportunity_id,
                due,
                "High",
                "Not Started",
                "Sales",
                "On Due Date",
                now_iso(),
            ),
        )
    conn.commit()
    return None


def update_opportunity_status(conn, opportunity_id, new_status, reason_loss=None, loss_notes=None):
    opp = conn.execute("SELECT status, actual_close_date FROM opportunity WHERE id=?", (opportunity_id,)).fetchone()
    if not opp:
        return "Opportunity not found"
    prob = None
    actual_close = opp["actual_close_date"]
    if new_status == "Won":
        prob = 100
        if not actual_close:
            actual_close = date.today().isoformat()
    elif new_status in ["Lost", "Cancelled"]:
        prob = 0
        if new_status == "Lost" and not reason_loss:
            return "Reason for loss is required"
        if not actual_close:
            actual_close = date.today().isoformat()
    conn.execute(
        """
        UPDATE opportunity SET status=?, probability=COALESCE(?,probability), reason_for_loss=?, loss_notes=?, actual_close_date=?
        WHERE id=?
        """,
        (new_status, prob, reason_loss, loss_notes, actual_close, opportunity_id),
    )
    activity_log(conn, "Opportunity", opportunity_id, "Status change", f"{opp['status']} -> {new_status}")
    conn.commit()
    return None


def run_idle_automation(conn, days_in_stage=21):
    rows = conn.execute(
        """
        SELECT id,name,stage_entered_date FROM opportunity
        WHERE status='Open' AND stage_entered_date IS NOT NULL
          AND julianday('now') - julianday(stage_entered_date) > ?
        """,
        (days_in_stage,),
    ).fetchall()
    created = 0
    for r in rows:
        exists = conn.execute(
            "SELECT COUNT(*) c FROM task WHERE linked_to_type='Opportunity' AND linked_to_id=? AND title='Stage stale follow-up' AND status != 'Completed'",
            (r["id"],),
        ).fetchone()["c"]
        if exists == 0:
            conn.execute(
                """
                INSERT INTO task(title,description,linked_to_type,linked_to_id,due_date,priority,status,role_related_to,reminder,created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    "Stage stale follow-up",
                    f"Opportunity '{r['name']}' stalled in stage",
                    "Opportunity",
                    r["id"],
                    (date.today() + timedelta(days=1)).isoformat(),
                    "High",
                    "Not Started",
                    "Sales",
                    "On Due Date",
                    now_iso(),
                ),
            )
            created += 1
    conn.commit()
    return created


def create_tender_date_reminders(conn, reminder_days=3):
    dates = ["site_visit_datetime", "clarification_deadline", "submission_datetime", "bid_bond_expiry_date"]
    created = 0
    for field in dates:
        rows = conn.execute(
            f"""
            SELECT id,name,{field} AS d FROM tender
            WHERE {field} IS NOT NULL
              AND date({field}) = date('now', ?)
            """,
            (f"+{reminder_days} day",),
        ).fetchall()
        for r in rows:
            exists = conn.execute(
                "SELECT COUNT(*) c FROM task WHERE linked_to_type='Tender' AND linked_to_id=? AND title=?",
                (r["id"], f"Tender reminder: {field}"),
            ).fetchone()["c"]
            if exists == 0:
                conn.execute(
                    """
                    INSERT INTO task(title,description,linked_to_type,linked_to_id,due_date,priority,status,role_related_to,reminder,created_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        f"Tender reminder: {field}",
                        f"{r['name']} has {field} on {r['d']}",
                        "Tender",
                        r["id"],
                        date.today().isoformat(),
                        "High",
                        "Not Started",
                        "Presales",
                        "On Due Date",
                        now_iso(),
                    ),
                )
                created += 1
    conn.commit()
    return created


def derive_key(password: str):
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def make_encrypted_backup(password: str):
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"crm_backup_{ts}.bin"
    raw = DB_PATH.read_bytes()
    cipher = Fernet(derive_key(password))
    encrypted = cipher.encrypt(raw)
    backup_file.write_bytes(encrypted)
    backups = sorted(BACKUP_DIR.glob("crm_backup_*.bin"), reverse=True)
    for old in backups[10:]:
        old.unlink(missing_ok=True)
    return backup_file


def restore_backup(path: str, password: str):
    cipher = Fernet(derive_key(password))
    encrypted = Path(path).read_bytes()
    raw = cipher.decrypt(encrypted)
    DB_PATH.write_bytes(raw)


def df(conn, sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)


def dashboard(conn):
    st.subheader("Home Dashboard")
    col1, col2, col3 = st.columns(3)
    pipe = conn.execute("SELECT COALESCE(SUM(estimated_deal_value),0) v FROM opportunity WHERE status='Open'").fetchone()["v"]
    month_forecast = conn.execute(
        """
        SELECT COALESCE(SUM(estimated_deal_value * probability / 100.0),0) v
        FROM opportunity
        WHERE status='Open' AND forecast_category != 'Omitted'
          AND strftime('%Y-%m', expected_close_date)=strftime('%Y-%m','now')
        """
    ).fetchone()["v"]
    due_today = conn.execute(
        "SELECT COUNT(*) c FROM task WHERE status != 'Completed' AND due_date=date('now')"
    ).fetchone()["c"]
    col1.metric("Total Pipeline", f"SAR {pipe:,.0f}")
    col2.metric("This Month Forecast", f"SAR {month_forecast:,.0f}")
    col3.metric("Tasks Due Today", int(due_today))

    st.write("#### Pipeline by Stage")
    st.dataframe(
        df(
            conn,
            """
            SELECT stage, COUNT(*) as opportunities, COALESCE(SUM(estimated_deal_value),0) as value
            FROM opportunity WHERE status='Open'
            GROUP BY stage ORDER BY opportunities DESC
            """,
        ),
        use_container_width=True,
    )

    st.write("#### Forecast Breakdown")
    st.dataframe(
        df(
            conn,
            """
            SELECT forecast_category, COALESCE(SUM(estimated_deal_value * probability / 100.0),0) as forecast_value
            FROM opportunity WHERE status='Open' AND forecast_category != 'Omitted'
            GROUP BY forecast_category
            """,
        ),
        use_container_width=True,
    )

    st.write("#### Top 10 Live Opportunities")
    st.dataframe(
        df(
            conn,
            """
            SELECT o.id,o.name,c.name client,o.stage,o.status,o.estimated_deal_value,o.expected_close_date,o.next_action_date
            FROM opportunity o JOIN client c ON c.id=o.client_id
            WHERE o.status in ('Open','On Hold')
            ORDER BY o.estimated_deal_value DESC LIMIT 10
            """,
        ),
        use_container_width=True,
    )

    st.write("#### Upcoming Tender Dates (next 14 days)")
    st.dataframe(
        df(
            conn,
            """
            SELECT id,name,submission_datetime,clarification_deadline,site_visit_datetime,bid_bond_expiry_date,tender_status
            FROM tender
            WHERE date(submission_datetime) <= date('now','+14 day')
               OR date(clarification_deadline) <= date('now','+14 day')
               OR date(site_visit_datetime) <= date('now','+14 day')
            ORDER BY submission_datetime
            """,
        ),
        use_container_width=True,
    )

    st.write("#### Recent Interactions")
    st.dataframe(
        df(
            conn,
            """
            SELECT i.date_time,c.name client,i.type,i.summary,i.outcome
            FROM interaction i JOIN client c ON c.id=i.client_id
            ORDER BY i.date_time DESC LIMIT 10
            """,
        ),
        use_container_width=True,
    )


def forms(conn):
    tab_names = ["Quick Add", "Clients", "Opportunities", "Tenders", "Tasks", "Interactions", "Vendors", "Data Hygiene"]
    quick, clients_tab, opp_tab, tender_tab, task_tab, inter_tab, vendor_tab, hygiene_tab = st.tabs(tab_names)

    with quick:
        st.write("Quick Add (<10 seconds)")
        qcol1, qcol2 = st.columns(2)
        with qcol1:
            with st.form("qa_task"):
                title = st.text_input("Task title")
                due = st.date_input("Due", value=date.today())
                if st.form_submit_button("Add Task") and title:
                    conn.execute(
                        "INSERT INTO task(title,due_date,status,priority,linked_to_type,created_at) VALUES(?,?,?,?,?,?)",
                        (title, due.isoformat(), "Not Started", "Medium", "General", now_iso()),
                    )
                    conn.commit()
                    st.success("Task created")
        with qcol2:
            with st.form("qa_interaction"):
                clients = conn.execute("SELECT id,name FROM client ORDER BY name").fetchall()
                if clients:
                    cl = st.selectbox("Client", clients, format_func=lambda x: x["name"], key="qa_client")
                    summary = st.text_input("Interaction summary")
                    if st.form_submit_button("Add Interaction") and summary:
                        conn.execute(
                            "INSERT INTO interaction(date_time,type,direction,client_id,summary) VALUES(?,?,?,?,?)",
                            (now_iso(), "Call", "Outbound", cl["id"], summary),
                        )
                        conn.commit()
                        st.success("Interaction logged")
                else:
                    st.info("Create a client first")

    with clients_tab:
        st.write("Create Client Group / Client / Contact")
        with st.form("client_group_form"):
            c1, c2 = st.columns(2)
            gname = c1.text_input("Client Group Name")
            gtype = c2.selectbox("Type", ["Government", "Semi-government", "Private"])
            gnotes = st.text_area("Notes")
            if st.form_submit_button("Add Client Group") and gname:
                conn.execute("INSERT OR IGNORE INTO client_group(name,type,notes) VALUES(?,?,?)", (gname, gtype, gnotes))
                conn.commit()

        groups = conn.execute("SELECT id,name FROM client_group ORDER BY name").fetchall()
        with st.form("client_form"):
            name = st.text_input("Client Name")
            gid = st.selectbox("Linked Client Group", groups, format_func=lambda x: x["name"] if x else "", index=None)
            sector = st.selectbox("Sector", ["Government", "Semi-government", "Private"])
            region = st.selectbox("Region", ["Eastern", "Riyadh", "Other"])
            priority = st.selectbox("Priority", ["Strategic", "VIP", "Normal", "Low", "Opportunistic"])
            div = st.selectbox("Main Division", ["DC", "AV", "IT", "Events", "Low Current"])
            status = st.selectbox("Status", ["Active", "Dormant", "Prospect"])
            notes = st.text_area("Notes", key="client_notes")
            if st.form_submit_button("Add Client") and name:
                conn.execute(
                    "INSERT INTO client(name,client_group_id,sector,region,account_priority,division_focus,status,notes) VALUES(?,?,?,?,?,?,?,?)",
                    (name, gid["id"] if gid else None, sector, region, priority, div, status, notes),
                )
                conn.commit()

        clients = conn.execute("SELECT id,name FROM client ORDER BY name").fetchall()
        with st.form("contact_form"):
            client = st.selectbox("Client", clients, format_func=lambda x: x["name"] if x else "", index=None)
            cname = st.text_input("Contact Name")
            role = st.selectbox("Role", ["IT Manager", "CEO", "GM", "Finance", "Procurement", "Consultant", "Other"])
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            channel = st.selectbox("Preferred Channel", ["Call", "Email", "WhatsApp", "Other"])
            notes = st.text_area("Relationship/Influence Notes")
            if st.form_submit_button("Add Contact") and client and cname:
                conn.execute(
                    "INSERT INTO contact(client_id,name,role,email,phone,preferred_channel,notes) VALUES(?,?,?,?,?,?,?)",
                    (client["id"], cname, role, normalize_email(email), normalize_phone(phone), channel, notes),
                )
                conn.commit()

        st.dataframe(df(conn, "SELECT id,name,region,status,account_priority FROM client ORDER BY id DESC LIMIT 100"), use_container_width=True)

    with opp_tab:
        clients = conn.execute("SELECT id,name,account_priority,region FROM client ORDER BY name").fetchall()
        tenders = conn.execute("SELECT id,name FROM tender ORDER BY id DESC").fetchall()
        with st.form("opportunity_form"):
            name = st.text_input("Opportunity Name")
            client = st.selectbox("Client", clients, format_func=lambda x: x["name"], index=None)
            division = st.selectbox("Division", ["DC", "AV", "IT", "Events", "Low Current"])
            region = st.selectbox("Region", ["Eastern", "Riyadh", "Other"])
            optype = st.selectbox("Type", ["Tender", "Direct", "Renewal", "Upsell", "Other"])
            source = st.selectbox("Source", ["Existing client", "Public tender", "Partner referral", "Company email RFQ", "Market intel", "Cold outreach"])
            stage = st.selectbox("Stage", OPEN_STAGES)
            deal = st.number_input("Estimated Deal Value", min_value=0.0)
            expected = st.date_input("Expected Close Date", value=date.today() + timedelta(days=30))
            next_action = st.date_input("Next Action Date", value=date.today() + timedelta(days=7))
            fc = st.selectbox("Forecast Category", ["Commit", "Best Case", "Pipeline", "Omitted"])
            linked_tender = st.selectbox("Linked Tender", tenders, format_func=lambda x: x["name"], index=None)
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Opportunity") and name and client:
                conn.execute(
                    """
                    INSERT INTO opportunity(name,client_id,division,region,account_priority,opportunity_type,source,stage,probability,
                    stage_entered_date,status,estimated_deal_value,expected_close_date,next_action_date,forecast_category,date_identified,linked_tender_id,notes)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        name,
                        client["id"],
                        division,
                        region,
                        client["account_priority"],
                        optype,
                        source,
                        stage,
                        STAGE_PROBABILITY.get(stage, 20),
                        date.today().isoformat(),
                        "Open",
                        deal,
                        expected.isoformat(),
                        next_action.isoformat(),
                        fc,
                        date.today().isoformat(),
                        linked_tender["id"] if linked_tender else None,
                        notes,
                    ),
                )
                conn.commit()

        st.write("Stage / Status Management")
        opps = conn.execute("SELECT id,name,stage,status FROM opportunity ORDER BY id DESC LIMIT 200").fetchall()
        if opps:
            selected = st.selectbox("Select Opportunity", opps, format_func=lambda x: f"#{x['id']} {x['name']} ({x['stage']}/{x['status']})")
            c1, c2 = st.columns(2)
            new_stage = c1.selectbox("New Stage", OPEN_STAGES)
            if c1.button("Apply Stage"):
                err = update_opportunity_stage(conn, selected["id"], new_stage)
                if err:
                    st.error(err)
                else:
                    st.success("Stage updated")
            new_status = c2.selectbox("New Status", ["Open", "Won", "Lost", "Cancelled", "On Hold"])
            loss_reason = c2.selectbox("Loss Reason", [None] + LOSS_REASONS)
            loss_notes = c2.text_input("Loss notes")
            if c2.button("Apply Status"):
                err = update_opportunity_status(conn, selected["id"], new_status, loss_reason, loss_notes)
                if err:
                    st.error(err)
                else:
                    st.success("Status updated")

        st.dataframe(
            df(
                conn,
                """
                SELECT o.id,o.name,c.name client,o.stage,o.status,o.probability,o.estimated_deal_value,
                (o.estimated_deal_value*o.probability/100.0) forecast_value,o.expected_close_date,o.last_activity_date
                FROM opportunity o JOIN client c ON c.id=o.client_id
                ORDER BY o.id DESC
                """,
            ),
            use_container_width=True,
        )

    with tender_tab:
        clients = conn.execute("SELECT id,name FROM client ORDER BY name").fetchall()
        opps = conn.execute("SELECT id,name FROM opportunity ORDER BY id DESC").fetchall()
        with st.form("tender_form"):
            name = st.text_input("Tender Name")
            ref = st.text_input("Reference/Number")
            client = st.selectbox("Issuing Client", clients, format_func=lambda x: x["name"], index=None)
            linked_opp = st.selectbox("Linked Opportunity", opps, format_func=lambda x: x["name"], index=None)
            role = st.selectbox("Role", ["Prime", "Subcontractor"])
            prime_name = st.text_input("Prime company (if sub)")
            sub_date = st.date_input("Submission Date", value=date.today() + timedelta(days=14))
            clar = st.date_input("Clarification Deadline", value=date.today() + timedelta(days=7))
            status = st.selectbox("Tender Status", ["Under Study", "In Preparation", "Submitted", "Awaiting Result", "Awarded", "Lost", "Cancelled", "Postponed", "No Participation"])
            reason = st.selectbox("Reason for loss/no participation", [None] + NO_PARTICIPATION_REASONS)
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Tender") and name and client:
                conn.execute(
                    """
                    INSERT INTO tender(name,reference_number,issuing_client_id,linked_opportunity_id,role,prime_company_name,
                    submission_datetime,clarification_deadline,tender_status,reason_for_loss_no_participation,notes)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        name,
                        ref,
                        client["id"],
                        linked_opp["id"] if linked_opp else None,
                        role,
                        prime_name,
                        sub_date.isoformat(),
                        clar.isoformat(),
                        status,
                        reason,
                        notes,
                    ),
                )
                conn.commit()

        st.dataframe(df(conn, "SELECT id,name,reference_number,tender_status,submission_datetime FROM tender ORDER BY id DESC"), use_container_width=True)

    with task_tab:
        with st.form("task_form"):
            title = st.text_input("Title")
            desc = st.text_area("Description")
            linked_type = st.selectbox("Linked To", ["Opportunity", "Tender", "Client", "Vendor", "General"])
            linked_id = st.number_input("Linked ID", min_value=0, step=1)
            due = st.date_input("Due Date", value=date.today() + timedelta(days=2))
            pri = st.selectbox("Priority", ["Low", "Medium", "High"])
            status = st.selectbox("Status", ["Not Started", "In Progress", "Waiting on Someone", "Completed", "Cancelled"])
            role = st.selectbox("Role", ["Client", "Presales", "Sales", "BD", "Finance", "Management", "Vendor", "Logistics", "HR", "Other"])
            wait = st.text_input("Waiting On")
            rem = st.selectbox("Reminder", ["None", "On Due Date", "2 days before", "Recurring weekly until done"])
            if st.form_submit_button("Add Task") and title:
                conn.execute(
                    """
                    INSERT INTO task(title,description,linked_to_type,linked_to_id,due_date,priority,status,role_related_to,waiting_on,reminder,created_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (title, desc, linked_type, linked_id, due.isoformat(), pri, status, role, wait, rem, now_iso()),
                )
                conn.commit()

        tdf = df(conn, "SELECT id,title,linked_to_type,linked_to_id,due_date,priority,status FROM task ORDER BY due_date")
        st.dataframe(tdf, use_container_width=True)

    with inter_tab:
        clients = conn.execute("SELECT id,name FROM client ORDER BY name").fetchall()
        opps = conn.execute("SELECT id,name FROM opportunity ORDER BY id DESC").fetchall()
        tenders = conn.execute("SELECT id,name FROM tender ORDER BY id DESC").fetchall()
        with st.form("interaction_form"):
            dt = st.text_input("Date & Time (ISO)", value=now_iso())
            itype = st.selectbox("Type", ["Call", "Meeting", "Email", "WhatsApp", "Site Visit", "Demo", "Workshop", "Clarification", "Internal Review", "Other"])
            direction = st.selectbox("Direction", ["Outbound", "Inbound"])
            client = st.selectbox("Client", clients, format_func=lambda x: x["name"], index=None)
            opp = st.selectbox("Linked Opportunity", opps, format_func=lambda x: x["name"], index=None)
            ten = st.selectbox("Linked Tender", tenders, format_func=lambda x: x["name"], index=None)
            summary = st.text_input("Summary")
            dnotes = st.text_area("Detailed Notes")
            outcome = st.text_input("Outcome")
            next_step = st.text_input("Next Step")
            next_step_date = st.date_input("Next Step Date", value=None)
            email_link = st.text_input("Email Reference Link")
            location = st.text_input("Location")
            make_task = st.checkbox("Create follow-up task if next step date provided", value=True)
            if st.form_submit_button("Add Interaction") and client and summary:
                conn.execute(
                    """
                    INSERT INTO interaction(date_time,type,direction,client_id,linked_opportunity_id,linked_tender_id,summary,detailed_notes,
                    outcome,next_step,next_step_date,email_reference_link,location)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        dt,
                        itype,
                        direction,
                        client["id"],
                        opp["id"] if opp else None,
                        ten["id"] if ten else None,
                        summary,
                        dnotes,
                        outcome,
                        next_step,
                        next_step_date.isoformat() if next_step_date else None,
                        email_link,
                        location,
                    ),
                )
                if opp:
                    conn.execute(
                        "UPDATE opportunity SET last_activity_date=? WHERE id=?",
                        (date.today().isoformat(), opp["id"]),
                    )
                if make_task and next_step_date:
                    conn.execute(
                        """
                        INSERT INTO task(title,description,linked_to_type,linked_to_id,due_date,priority,status,role_related_to,reminder,created_at)
                        VALUES(?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            f"Follow-up: {summary}",
                            next_step,
                            "Opportunity" if opp else "Client",
                            opp["id"] if opp else client["id"],
                            next_step_date.isoformat(),
                            "Medium",
                            "Not Started",
                            "Sales",
                            "On Due Date",
                            now_iso(),
                        ),
                    )
                conn.commit()

        st.dataframe(df(conn, "SELECT id,date_time,type,direction,client_id,summary,next_step_date FROM interaction ORDER BY date_time DESC LIMIT 200"), use_container_width=True)

    with vendor_tab:
        with st.form("vendor_form"):
            name = st.text_input("Vendor Name")
            typ = st.selectbox("Type", ["Vendor", "Distributor", "Technology Partner", "Contractor"])
            tier = st.text_input("Partner Tier")
            territory = st.text_input("Territory")
            lines = st.text_area("Product/Solution lines")
            pay_terms = st.text_input("Default Vendor Payment Terms")
            dr_possible = st.checkbox("Deal Registration Possible")
            dr_status = st.selectbox("Deal Registration Status", ["Not Started", "In Progress", "Approved", "Rejected", "Expired"])
            nda_status = st.selectbox("NDA Status", ["Not Signed", "Signed", "Expired"])
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Vendor") and name:
                conn.execute(
                    """
                    INSERT INTO vendor(name,type,partner_tier,territory_region,product_lines,default_vendor_payment_terms,
                    deal_registration_possible,deal_registration_status,nda_status,notes)
                    VALUES(?,?,?,?,?,?,?,?,?,?)
                    """,
                    (name, typ, tier, territory, lines, pay_terms, int(dr_possible), dr_status, nda_status, notes),
                )
                conn.commit()

        st.dataframe(
            df(
                conn,
                """
                SELECT v.id,v.name,v.type,v.deal_registration_status,
                COALESCE((SELECT SUM(o.estimated_deal_value) FROM opportunity_vendor ov JOIN opportunity o ON o.id=ov.opportunity_id WHERE ov.vendor_id=v.id AND o.status='Open'),0) pipeline_value,
                COALESCE((SELECT SUM(o.estimated_deal_value) FROM opportunity_vendor ov JOIN opportunity o ON o.id=ov.opportunity_id WHERE ov.vendor_id=v.id AND o.status='Won'),0) awarded_value
                FROM vendor v ORDER BY v.id DESC
                """,
            ),
            use_container_width=True,
        )

    with hygiene_tab:
        st.write("Duplicate Suggestions")
        st.write("Contacts with same email")
        st.dataframe(
            df(
                conn,
                """
                SELECT email, COUNT(*) c, GROUP_CONCAT(name, ', ') names
                FROM contact WHERE email IS NOT NULL AND email != ''
                GROUP BY email HAVING COUNT(*) > 1
                """,
            ),
            use_container_width=True,
        )
        st.write("Potential duplicate clients (same first 6 letters)")
        st.dataframe(
            df(
                conn,
                """
                SELECT substr(lower(name),1,6) key, COUNT(*) c, GROUP_CONCAT(name, ', ') names
                FROM client GROUP BY key HAVING COUNT(*) > 1
                """,
            ),
            use_container_width=True,
        )
        st.write("Duplicate tender references")
        st.dataframe(
            df(
                conn,
                """
                SELECT reference_number, COUNT(*) c, GROUP_CONCAT(name, ', ') names
                FROM tender WHERE reference_number IS NOT NULL AND reference_number != ''
                GROUP BY reference_number HAVING COUNT(*) > 1
                """,
            ),
            use_container_width=True,
        )


def integrations(conn):
    st.subheader("Integrations (Offline-first references)")
    st.write("Use deep links only. CRM keeps source-of-truth locally.")
    with st.expander("Simulate Create from Email"):
        sender = st.text_input("Sender Email")
        subject = st.text_input("Email Subject")
        body_summary = st.text_area("Body Summary")
        email_ref = st.text_input("Email Deep Link")
        action = st.selectbox("Create", ["Opportunity", "Task", "Interaction"])
        if st.button("Process Email"):
            contact = conn.execute("SELECT * FROM contact WHERE email=?", (normalize_email(sender),)).fetchone()
            if not contact:
                conn.execute(
                    "INSERT INTO unmatched_sender(sender_email,summary,source_ref,created_at) VALUES(?,?,?,?)",
                    (normalize_email(sender), body_summary, email_ref, now_iso()),
                )
                conn.commit()
                st.warning("No contact match; added to Unmatched Sender queue.")
            else:
                if action == "Opportunity":
                    conn.execute(
                        """
                        INSERT INTO opportunity(name,client_id,stage,probability,status,date_identified,stage_entered_date,notes)
                        VALUES(?,?,?,?,?,?,?,?)
                        """,
                        (subject, contact["client_id"], "Lead", 20, "Open", date.today().isoformat(), date.today().isoformat(), body_summary),
                    )
                elif action == "Task":
                    conn.execute(
                        "INSERT INTO task(title,description,linked_to_type,linked_to_id,status,priority,created_at) VALUES(?,?,?,?,?,?,?)",
                        (subject, body_summary, "Client", contact["client_id"], "Not Started", "Medium", now_iso()),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO interaction(date_time,type,direction,client_id,summary,detailed_notes,email_reference_link)
                        VALUES(?,?,?,?,?,?,?)
                        """,
                        (now_iso(), "Email", "Inbound", contact["client_id"], subject, body_summary, email_ref),
                    )
                conn.commit()
                st.success("Created successfully")

    st.write("#### Unmatched Sender Queue")
    st.dataframe(df(conn, "SELECT * FROM unmatched_sender ORDER BY created_at DESC"), use_container_width=True)


def settings_and_backup(conn):
    st.subheader("Settings, Backup, Restore")
    c1, c2 = st.columns(2)
    with c1:
        st.write("Automation")
        days_stage = st.number_input("Stalled opportunity threshold (days)", min_value=1, value=21)
        reminder_days = st.number_input("Tender reminder lead (days)", min_value=1, value=3)
        if st.button("Run automations now"):
            a = run_idle_automation(conn, days_stage)
            b = create_tender_date_reminders(conn, reminder_days)
            st.success(f"Created {a} stalled tasks and {b} tender reminder tasks")

        st.write("Data export")
        table = st.selectbox("Export table", ["client", "contact", "opportunity", "tender", "task", "interaction", "vendor"])
        if st.button("Export CSV"):
            export_df = df(conn, f"SELECT * FROM {table}")
            st.download_button(
                f"Download {table}.csv",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name=f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )

    with c2:
        st.write("Encrypted backups")
        backup_password = st.text_input("Backup password", type="password")
        if st.button("Create encrypted backup"):
            if not backup_password:
                st.error("Enter a backup password")
            else:
                p = make_encrypted_backup(backup_password)
                st.success(f"Backup created: {p}")

        backup_files = sorted(BACKUP_DIR.glob("crm_backup_*.bin"), reverse=True)
        selected = st.selectbox("Restore from backup", [str(p) for p in backup_files], index=None)
        restore_password = st.text_input("Restore password", type="password")
        if st.button("Restore selected backup"):
            if selected and restore_password:
                try:
                    restore_backup(selected, restore_password)
                    st.success("Backup restored. Reload app.")
                except Exception as e:
                    st.error(f"Restore failed: {e}")


def main():
    st.set_page_config(page_title="Personal CRM Cockpit", layout="wide")
    init_db()

    st.title("Personal CRM Cockpit (Single-User, Offline-First)")
    with closing(get_conn()) as conn:
        nav = st.sidebar.radio(
            "Navigate",
            ["Dashboard", "CRM Workspace", "Integrations", "Settings & Backup", "Data Model"],
        )
        if nav == "Dashboard":
            dashboard(conn)
        elif nav == "CRM Workspace":
            forms(conn)
        elif nav == "Integrations":
            integrations(conn)
        elif nav == "Settings & Backup":
            settings_and_backup(conn)
        else:
            st.subheader("Architecture and Sync/Conflict Model")
            st.markdown(
                """
                - **Local-first DB:** SQLite is source of truth for all CRM entities.
                - **Audit separation:** `activity_log` tracks system changes; `interaction` tracks human touchpoints.
                - **Integrations as references:** only email/event links are stored (no full body/content).
                - **Manual + scheduled sync-ready:** UI supports manual ingestion; scheduler can call same methods.
                - **Conflict handling:** CRM keeps local values; broken external links are shown but data remains.
                - **Data quality:** stage-gates, duplicate suggestions, normalized email/phone.
                - **Safety:** encrypted backup/restore and rotating backup retention.
                """
            )
            st.code("sqlite3 personal_crm.db '.schema'", language="bash")


if __name__ == "__main__":
    main()
