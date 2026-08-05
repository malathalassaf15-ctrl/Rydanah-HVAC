# 🔧 Rydanah HVAC — Customer & Job Tracker

A lightweight internal tool built for Rydanah HVAC to organize customer intake, job requests, and real-time job status — replacing manual tracking with a single, searchable dashboard.

---
## 🎯 The Problem
Managing HVAC service calls manually — customer details, technician assignments, job progress — makes it easy to lose track of where each job actually stands, especially across multiple active customers at once. This tool centralizes:
* **Customer intake:** name, contact info, company, date of first contact
* **Job details:** customer request, action plan, assigned technician, technician feedback
* **Live status tracking:** a customizable progress stage for every job, from first contact to completion

---
## ✨ Key Features
* **Structured intake form** for new customers and jobs, including a WhatsApp-contact tracker
* **Editable status pipeline** — comes with default stages (Technician Sent → Quotation → Waiting for Approval → In Progress → Completed), with the ability to add custom stages on the fly
* **Status filtering** to instantly view all jobs at a given stage
* **Job status breakdown chart** for an at-a-glance view of how many jobs are in each stage

---
## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Streamlit
* **Data Handling:** Pandas

---
## 🚀 How to Run Locally
1. Clone the repository:
```bash
   git clone https://github.com/malathalassaf15-ctrl/Rydanah-HVAC.git
```
2. Navigate into the project folder:
```bash
   cd Rydanah-HVAC
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Launch the app:
```bash
   streamlit run app.py
```

---
## 📌 Note
This version stores job data in-session for demonstration purposes. A production version would connect to persistent storage (e.g. a CSV file or database) so job records carry over between sessions.
