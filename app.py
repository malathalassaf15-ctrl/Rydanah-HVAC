import pandas as pd
import streamlit as st
import os
from datetime import date

st.set_page_config(page_title="Rydanah HVAC — Customer & Job Tracker", layout="wide")
st.title("🔧 Rydanah HVAC — Customer & Job Tracker")
st.write("Track customer intake, job requests, and real-time job status in one place.")

DATA_FILE = "jobs_data.csv"
STAGES_FILE = "custom_stages.csv"

DEFAULT_STAGES = [
    "Technician Sent",
    "Quotation",
    "Waiting for Approval",
    "In Progress",
    "Completed",
]

COLUMNS = [
    "Customer Name",
    "Phone Number",
    "Company Name",
    "Date of Contact",
    "WhatsApp Sent",
    "Customer Request",
    "Action Plan",
    "Technician Assigned",
    "Technician Feedback",
    "Status",
]


def load_jobs():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_jobs(df):
    df.to_csv(DATA_FILE, index=False)


def load_custom_stages():
    if os.path.exists(STAGES_FILE):
        return pd.read_csv(STAGES_FILE)["Stage"].tolist()
    return []


def save_custom_stages(stages):
    pd.DataFrame({"Stage": stages}).to_csv(STAGES_FILE, index=False)


# Load from disk on every run — this is what fixes the refresh-wipes-data issue
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

    st.markdown("**Need a stage that's not listed?**")
    new_stage = st.text_input("Add a new stage (optional)")

    submitted = st.form_submit_button("Add Job")

    if submitted:
        if not name.strip():
            st.error("Customer Name is required.")
        else:
            if new_stage.strip():
                if new_stage.strip() not in custom_stages:
                    custom_stages.append(new_stage.strip())
                    save_custom_stages(custom_stages)
                status = new_stage.strip()

            new_row = pd.DataFrame(
                [
                    {
                        "Customer Name": name,
                        "Phone Number": phone,
                        "Company Name": company,
                        "Date of Contact": contact_date,
                        "WhatsApp Sent": "Yes" if whatsapp_sent else "No",
                        "Customer Request": request,
                        "Action Plan": action_plan,
                        "Technician Assigned": technician,
                        "Technician Feedback": feedback,
                        "Status": status,
                    }
                ]
            )
            jobs_df = pd.concat([jobs_df, new_row], ignore_index=True)
            save_jobs(jobs_df)
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
        jobs_df.loc[job_index, "Status"] = new_status
        save_jobs(jobs_df)
        st.success("Status updated.")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Job Status Breakdown")
    status_counts = jobs_df["Status"].value_counts()
    st.bar_chart(status_counts)
