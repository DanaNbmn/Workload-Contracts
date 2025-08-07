import streamlit as st
from docx import Document
from io import BytesIO
import json

# Load the benefits data from a JSON file
with open("benefits_by_profile.json", "r") as f:
    benefits_data = json.load(f)

# Streamlit UI
st.set_page_config(page_title="Faculty Contract Generator", layout="centered")
st.title("📄 Faculty Offer Letter Generator")
st.markdown("Please fill out the information below and the contract will be generated automatically.")

# FORM INPUTS
with st.form("contract_form"):
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Candidate Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    position_title = st.selectbox("Position Title (Rank)", [
        "Professor", "Associate Professor", "Assistant Professor", "Senior Instructor", "Instructor"
    ])
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    campus = st.selectbox("Campus", ["Al Ain", "AD/Dubai"])
    department = st.text_input("College / Department")
    reporting_manager = st.text_input("Reporting Manager")
    total_salary = st.text_input("Total Salary (AED)")
    probation = st.text_input("Probation Period (in months)", value="6")
    international_hire = st.checkbox("International Hire", value=True)
    submitted = st.form_submit_button("Generate Contract")

if submitted:
    profile_key = f"{position_title} – {campus} – {marital_status}"
    benefits = benefits_data.get(profile_key, {})

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
        "joining_ticket": benefits.get("Joining Ticket", "N/A") if international_hire else "N/A",
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

    def generate_contract(data):
        template_path = "Faculty_Offer_Template.docx"
        doc = Document(template_path)
        for p in doc.paragraphs:
            for key, value in data.items():
                if f"{{{{{key}}}}}" in p.text:
                    inline = p.runs
                    for i in range(len(inline)):
                        if f"{{{{{key}}}}}" in inline[i].text:
                            inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(value))
        return doc

    final_doc = generate_contract(context)
    byte_io = BytesIO()
    final_doc.save(byte_io)
    byte_io.seek(0)

    st.success("✅ Contract generated successfully!")
    st.download_button(
        label="📥 Download Contract",
        data=byte_io,
        file_name=f"{name}_Contract.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

