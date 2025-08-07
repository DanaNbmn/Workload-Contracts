import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import json

# --- Constants ---
TEMPLATE_PATH = "Faculty_Offer_Template.docx"
BENEFITS_PATH = "benefits_by_profile.json"

# --- Load Benefits Profiles ---
@st.cache_data
def load_benefits():
    with open(BENEFITS_PATH, "r") as f:
        return json.load(f)

benefits_data = load_benefits()

# --- Helper Function to Generate Contract ---
def generate_contract(context):
    doc = Document(TEMPLATE_PATH)
    for p in doc.paragraphs:
        for key, value in context.items():
            if f"{{{{{key}}}}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if f"{{{{{key}}}}}" in inline[i].text:
                        inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(value))
    return doc

# --- UI ---
st.title("📄 Faculty Contract Generator")

st.markdown("Please fill out the required details below and select the applicable rank, campus, and marital status to generate the contract.")

with st.form("contract_form"):
    # Personal Details
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    position_title = st.text_input("Position Title")
    department = st.text_input("College/Department")
    reporting_manager = st.text_input("Reporting Manager")
    total_salary = st.text_input("Total Monthly Salary (AED)")
    probation = st.text_input("Probation Period (in months)", value="6")

    # Contract Logic Drivers
    rank = st.selectbox("Rank (Job Title)", [
        "Professor", "Associate Professor", "Assistant Professor", "Lecturer", "Senior Instructor", "Instructor"
    ])

    campus = st.selectbox("Campus", ["Al Ain", "Abu Dhabi", "Dubai"])
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])

    submitted = st.form_submit_button("Generate Contract")

    if submitted:
        profile_key = f"{rank} – {campus} – {marital_status}"
        benefits = benefits_data.get(profile_key, {})

        # --- Fill contract placeholders ---
        context = {
            "salutation": f"{position_title} {name}",
            "emp_id": emp_id,
            "email": email,
            "phone": phone,
            "position_title": department,
            "designation": position_title,
            "reporting_manager": reporting_manager,
            "total_salary": total_salary,
            "probation": probation,
            "joining_ticket": benefits.get("Joining Ticket", "N/A"),
            "housing_allowance": benefits.get("Housing Allowance", "N/A"),
            "furniture_allowance": benefits.get("Furniture Allowance", "N/A"),
            "school_allowance": benefits.get("Children School Allowance", "N/A"),
            "tuition_discount": benefits.get("Tuition Waiver Discount", "N/A"),
            "annual_ticket": benefits.get("Annual Ticket", "N/A"),
            "relocation_allowance": benefits.get("Relocation Allowance", "N/A"),
            "repatriation_allowance": benefits.get("Repatriation Allowance", "N/A"),
            "repatriation_ticket": benefits.get("Repatriation Ticket", "N/A"),
            "health_insurance": benefits.get("Health Insurance", "N/A"),
            "annual_leave": benefits.get("Annual Leave", "N/A"),
        }

        final_doc = generate_contract(context)
        byte_io = BytesIO()
        final_doc.save(byte_io)
        byte_io.seek(0)

        st.success("Contract generated successfully! Download below:")
        st.download_button(label="📥 Download Contract", data=byte_io, file_name=f"{name}_Contract.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
