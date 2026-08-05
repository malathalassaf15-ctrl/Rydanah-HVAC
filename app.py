import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date

st.set_page_config(page_title="Rydanah HVAC — Customer & Job Tracker", layout="wide")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_client():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return gspread.authorize(creds)

client = get_client()
sheet = client.open("Rydanah HVAC Jobs")
jobs_ws = sheet.sheet1
stages_ws = sheet.worksheet("Stages")

DEFAULT_STAGES = [
    "Technician Sent",
    "Quotation",
    "Waiting for Approval",
    "In Progress",
    "Completed",
]

COLUMNS = [
    "Customer Name", "Phone Number", "Company Name", "Date of Contact",
    "WhatsApp Sent", "Customer Request", "Action Plan",
    "Technician Assigned", "Technician Feedback", "Status",
]


def load_jobs():
    records = jobs_ws.get_all_records()
    if not records:
        return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(records)


def load_custom_stages():
    values = stages_ws.col_values(1)[1:]  # skip header
    return [v for v in values if v.strip()]


def add_custom_stage(stage):
    stages_ws.append_row([stage])


def append_job(row_dict):
    jobs_ws.append_row([row_dict[col] for col in COLUMNS])


def update_status(row_index, new_status):
    # +2 accounts for header row and 1-indexing
    status_col = COLUMNS.index("Status") + 1
    jobs_ws.update_cell(row_index + 2, status_col, new_status)


st.title("🔧 Rydanah HVAC — Customer & Job Tracker")
st.write("Track customer intake, job requests, and real-time job status in one place.")

jobs_df = load_jobs()
custom_stages = load_custom_stages()
all_stages = DEFAULT_STAGES + custom_stages

st.subheader("➕ Add New Customer / Job")
with st.form("new_job_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        company = st.text_input("Company Name")
        contact_date = st.date_input("Date of Contact", value=date.today())
        whatsapp_sent = st.checkbox("WhatsApp Message Sent to Owner")
    with col2:
        request = st.text_area("Customer Request")
        action_plan = st.text_area("Action Plan")
        technician = st.text_input("Technician Assigned")
        feedback = st.text_area("Technician Feedback")

    status = st.selectbox("Current Progress Stage", all_stages)
    new_stage = st.text_input("Add a new stage (optional)")

    submitted = st.form_submit_button("Add Job")

    if submitted:
        if not name.strip():
            st.error("Customer Name is required.")
        else:
            if new_stage.strip() and new_stage.strip() not in custom_stages:
                add_custom_stage(new_stage.strip())
                status = new_stage.strip()

            append_job({
                "Customer Name": name,
                "Phone Number": phone,
                "Company Name": company,
                "Date of Contact": str(contact_date),
                "WhatsApp Sent": "Yes" if whatsapp_sent else "No",
                "Customer Request": request,
                "Action Plan": action_plan,
                "Technician Assigned": technician,
                "Technician Feedback": feedback,
                "Status": status,
            })
            st.success(f"Added job for {name}.")
            st.rerun()

st.markdown("---")
st.subheader("📋 All Jobs")

if len(jobs_df) == 0:
    st.info("No jobs added yet. Use the form above to add your first customer.")
else:
    filter_status = st.selectbox("Filter by status", ["All"] + all_stages)
    display_df = jobs_df if filter_status == "All" else jobs_df[jobs_df["Status"] == filter_status]
    st.dataframe(display_df, use_container_width=True)

    st.markdown("---")
    st.subheader("🔄 Update Job Status")
    job_index = st.selectbox(
        "Select a job to update",
        jobs_df.index,
        format_func=lambda i: f"{jobs_df.loc[i, 'Customer Name']} — {jobs_df.loc[i, 'Status']}",
    )
    new_status = st.selectbox("New status", all_stages, key="update_status")
    if st.button("Update Status"):
        update_status(job_index, new_status)
        st.success("Status updated.")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Job Status Breakdown")
    st.bar_chart(jobs_df["Status"].value_counts())
