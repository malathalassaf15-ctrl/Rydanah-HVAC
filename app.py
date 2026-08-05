import pandas as pd
import streamlit as st
from datetime import date

st.set_page_config(page_title="Rydanah HVAC — Customer & Job Tracker", layout="wide")
st.title("🔧 Rydanah HVAC — Customer & Job Tracker")
st.write("Track customer intake, job requests, and real-time job status in one place.")

# Preset progress stages, editable by the user
DEFAULT_STAGES = [
    "Technician Sent",
    "Quotation",
    "Waiting for Approval",
    "In Progress",
    "Completed",
]

# Session-state storage acts as the in-memory "database" for this session
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame(
        columns=[
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
    )

if "custom_stages" not in st.session_state:
    st.session_state.custom_stages = []

all_stages = DEFAULT_STAGES + st.session_state.custom_stages

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
        if new_stage.strip():
            if new_stage not in st.session_state.custom_stages:
                st.session_state.custom_stages.append(new_stage.strip())
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
        st.session_state.jobs = pd.concat(
            [st.session_state.jobs, new_row], ignore_index=True
        )
        st.success(f"Added job for {name}.")

st.markdown("---")

st.subheader("📋 All Jobs")

if len(st.session_state.jobs) == 0:
    st.info("No jobs added yet. Use the form above to add your first customer.")
else:
    # Filter by status
    filter_status = st.selectbox(
        "Filter by status", ["All"] + all_stages
    )
    display_df = st.session_state.jobs
    if filter_status != "All":
        display_df = display_df[display_df["Status"] == filter_status]

    st.dataframe(display_df, use_container_width=True)

    st.markdown("---")
    st.subheader("🔄 Update Job Status")
    if len(st.session_state.jobs) > 0:
        job_index = st.selectbox(
            "Select a job to update (by row number)",
            st.session_state.jobs.index,
            format_func=lambda i: f"{st.session_state.jobs.loc[i, 'Customer Name']} — {st.session_state.jobs.loc[i, 'Status']}",
        )
        new_status = st.selectbox("New status", all_stages, key="update_status")
        if st.button("Update Status"):
            st.session_state.jobs.loc[job_index, "Status"] = new_status
            st.success("Status updated.")
            st.rerun()

    st.markdown("---")
    st.subheader("📊 Job Status Breakdown")
    status_counts = st.session_state.jobs["Status"].value_counts()
    st.bar_chart(status_counts)
