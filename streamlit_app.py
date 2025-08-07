import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# ----------------- Benefit Logic Table -----------------
def get_faculty_benefits(grade, campus, marital_status):
    table = {
        # Professor
        ("Professor", "Abu Dhabi / Dubai", "Single"):  {"HOUSING_ALLOWANCE": 45000, "FURNITURE_ALLOWANCE": 20000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Professor", "Abu Dhabi / Dubai", "Married"): {"HOUSING_ALLOWANCE": 60000, "FURNITURE_ALLOWANCE": 30000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Professor", "Al Ain", "Single"):             {"HOUSING_ALLOWANCE": 35000, "FURNITURE_ALLOWANCE": 20000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Professor", "Al Ain", "Married"):            {"HOUSING_ALLOWANCE": 45000, "FURNITURE_ALLOWANCE": 30000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},

        # Associate
        ("Associate / Sr. Lecturer", "Abu Dhabi / Dubai", "Single"):  {"HOUSING_ALLOWANCE": 45000, "FURNITURE_ALLOWANCE": 20000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Associate / Sr. Lecturer", "Abu Dhabi / Dubai", "Married"): {"HOUSING_ALLOWANCE": 60000, "FURNITURE_ALLOWANCE": 30000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Associate / Sr. Lecturer", "Al Ain", "Single"):             {"HOUSING_ALLOWANCE": 35000, "FURNITURE_ALLOWANCE": 20000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},
        ("Associate / Sr. Lecturer", "Al Ain", "Married"):            {"HOUSING_ALLOWANCE": 45000, "FURNITURE_ALLOWANCE": 30000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 3000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 56},

        # Instructor
        ("Instructor", "Abu Dhabi / Dubai", "Single"):  {"HOUSING_ALLOWANCE": 35000, "FURNITURE_ALLOWANCE": 12000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 2000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 42},
        ("Instructor", "Abu Dhabi / Dubai", "Married"): {"HOUSING_ALLOWANCE": 45000, "FURNITURE_ALLOWANCE": 15000, "SCHOOL_ALLOWANCE": 60000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 2000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 42},
        ("Instructor", "Al Ain", "Single"):             {"HOUSING_ALLOWANCE": 30000, "FURNITURE_ALLOWANCE": 12000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 2000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 42},
        ("Instructor", "Al Ain", "Married"):            {"HOUSING_ALLOWANCE": 40000, "FURNITURE_ALLOWANCE": 15000, "SCHOOL_ALLOWANCE": 50000, "TUITION_WAIVER": "75% Emp / 50% Dep / 25% Family", "RELOCATION_ALLOWANCE": 3000, "REPATRIATION_ALLOWANCE": 2000, "HEALTH_INSURANCE": "1+1+3", "ANNUAL_LEAVE_DAYS": 42},
    }
    return table.get((grade, campus, marital_status), {})

# ----------------- Generate Word Doc -----------------
def generate_contract(data, template_path="ADU_Faculty_Contract_Template.docx"):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, value in data.items():
            if f"{{{{{key}}}}}" in p.text:
                p.text = p.text.replace(f"{{{{{key}}}}}", str(value))
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ----------------- UI -----------------
st.title("📄 ADU Contract Generator")

# Manual Inputs
id_number = st.text_input("Faculty ID")
date = st.date_input("Contract Date")
name = st.text_input("Candidate Name")
email = st.text_input("Email ID")
phone = st.text_input("Phone Number")
rank = st.selectbox("Faculty Rank", ["Professor", "Associate / Sr. Lecturer", "Instructor"])
college = st.text_input("College/Department")
campus = st.selectbox("Campus", ["Abu Dhabi / Dubai", "Al Ain"])
marital = st.selectbox("Marital Status", ["Single", "Married"])
dean = st.text_input("Dean/Chair Name")
salary = st.number_input("Monthly Salary (AED)", step=1000)

# Button
if st.button("Generate Contract"):
    benefits = get_faculty_benefits(rank, campus, marital)
    if benefits:
        filled_data = {
            "ID_NUMBER": id_number,
            "DATE": date.strftime("%d-%b-%Y"),
            "CANDIDATE_NAME": name,
            "EMAIL_ID": email,
            "PHONE_NUMBER": phone,
            "RANK": rank,
            "COLLEGE": college,
            "CAMPUS": campus,
            "DEAN_CHAIR": dean,
            "SALARY": salary,
            **benefits
        }
        docx_file = generate_contract(filled_data)
        st.download_button("📥 Download Contract", docx_file, file_name=f"{name}_Faculty_Contract.docx")
    else:
        st.error("No benefit rule matched this selection. Please check your input.")
"""

# Save the updated Streamlit contract generator file
with open("/mnt/data/faculty_contract_generator_full.py", "w") as f:
    f.write(streamlit_contract_generator_code)

"/mnt/data/faculty_contract_generator_full.py"
