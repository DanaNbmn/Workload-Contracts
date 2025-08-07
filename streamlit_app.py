import streamlit as st
from docx import Document
from io import BytesIO
import datetime
import json

# Load benefit mappings
with open("benefits_by_profile.json", "r") as f:
    benefit_data = json.load(f)

# Load the contract template
TEMPLATE_PATH = "/mnt/data/Updated_Faculty_Offer_Template.docx"

def generate_contract(data):
    doc = Document(TEMPLATE_PATH)
    for p in doc.paragraphs:
        for key, value in data.items():
            if f"{{{{{key}}}}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if f"{{{{{key}}}}}" in inline[i].text:
                        inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(value))
    return doc

st.title("🎓 ADU Faculty Contract Generator")

# Input form
with st.form("contract_form"):
    st.subheader("Employee Information")
    candidate_id = st.text_input("Candidate ID")
    date_today = datetime.date.today().strftime("%d-%m-%Y")
    name = st.text_input("Candidate Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    designation = st.selectbox("Designation (Rank)", [
        "Professor", "Associate Professor / Sr. Lecturer", "Assistant Professor / Lecturer",
        "Senior Instructor", "Instructor"
    ])
    department = st.text_input("College/Department")
    reporting_manager = st.text_input("Reporting Manager")
    salary = st.text_input("Monthly Salary (AED)")
    probation = st.text_input("Probation Period (Months)", value="6")

    st.subheader("Employment Context")
    campus = st.selectbox("Campus", ["Al Ain", "AD/Dubai"])
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    is_international = st.radio("International Hire?", ["Yes", "No"])

    submitted = st.form_submit_button("Generate Contract")

    if submitted:
        key = f"{designation}|{campus}|{marital_status}"
        benefits = benefit_data.get(key, {})

        # Compose the dynamic inputs
        context = {
            "candidate_id": candidate_id,
            "date": date_today,
            "name": name,
            "phone": phone,
            "email": email,
            "designation": designation,
            "position_title": department,
            "reporting_manager": reporting_manager,
            "salary": salary,
            "probation": probation,
            "housing_allowance": benefits.get("housing_allowance", "N/A"),
            "furniture_allowance": benefits.get("furniture_allowance", "N/A"),
            "education_allowance": benefits.get("education_allowance", "N/A"),
            "annual_leave_days": benefits.get("annual_leave_days", "N/A"),
            "repatriation_allowance": benefits.get("repatriation_allowance", "N/A"),
            "international_joining": "commencement" if is_international == "Yes" else "",
        }

        final_doc = generate_contract(context)
        byte_io = BytesIO()
        final_doc.save(byte_io)
        byte_io.seek(0)

        st.success("✅ Contract generated successfully!")
        st.download_button(
            label="📥 Download Contract",
            data=byte_io,
            file_name=f"{candidate_id}_{name}_Contract.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

