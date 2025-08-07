import streamlit as st
from docx import Document
from io import BytesIO
import json

# Define benefit mapping directly (in lieu of external file for app portability)
benefits_data = {
    "Professor – Al Ain – Married": {
        "Joining Ticket": "1+1+2 Economy",
        "Housing Allowance": "AED 45,000",
        "Furniture Allowance": "AED 30,000",
        "Children School Allowance": "AED 50,000",
        "Tuition Waiver Discount": "75% / 50% / 25%",
        "Annual Ticket": "1+1+2 Economy",
        "Relocation Allowance": "AED 3,000",
        "Repatriation Allowance": "AED 3,000",
        "Repatriation Ticket": "1+1+2 Economy",
        "Health Insurance": "1+1+3",
        "Annual Leave": "56 days"
    },
    "Professor – AD/Dubai – Married": {
        "Joining Ticket": "1+1+2 Economy",
        "Housing Allowance": "AED 60,000",
        "Furniture Allowance": "AED 30,000",
        "Children School Allowance": "AED 60,000",
        "Tuition Waiver Discount": "75% / 50% / 25%",
        "Annual Ticket": "1+1+2 Economy",
        "Relocation Allowance": "AED 3,000",
        "Repatriation Allowance": "AED 3,000",
        "Repatriation Ticket": "1+1+2 Economy",
        "Health Insurance": "1+1+3",
        "Annual Leave": "56 days"
    }
    # Additional benefit profiles can be added here...
}

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
    rank = st.selectbox("Rank (for Benefits Mapping)", [
        "Professor", "Associate Professor", "Assistant Professor", "Senior Instructor", "Instructor"
    ])
    position_title = st.text_input("Position Title (to appear in contract)")
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    campus = st.selectbox("Campus", ["Al Ain", "AD/Dubai"])
    department = st.text_input("College / Department")
    reporting_manager = st.text_input("Reporting Manager")
    total_salary = st.text_input("Total Salary (AED)")
    probation = st.text_input("Probation Period (in months)", value="6")
    international_hire = st.checkbox("International Hire", value=True)
    submitted = st.form_submit_button("Generate Contract")

if submitted:
    profile_key = f"{rank} – {campus} – {marital_status}"
    benefits = benefits_data.get(profile_key, {})

    context = {
        "salutation": name,
        "emp_id": emp_id,
        "email": email,
        "phone": phone,
        "position_title": position_title,
        "designation": department,
        "reporting_manager": reporting_manager,
        "total_salary": total_salary,
        "probation": probation,
        "joining_ticket": benefits.get("Joining Ticket", "N/A") if international_hire else "N/A",
        "housing_allowance": benefits.get("Housing Allowance", "N/A"),
        "furniture_allowance": benefits.get("Furniture Allowance", "N/A"),
        "school_allowance": benefits.get("Children School Allowance", "N/A"),
        "tuition_discount": benefits.get("Tuition Waiver Discount", "N/A"),
        "annual_ticket": benefits.get("Annual Ticket", "N/A"),
        "relocation_allowance": benefits.get("Relocation Allowance", "N/A") if international_hire else "N/A",
        "repatriation_allowance": benefits.get("Repatriation Allowance", "N/A"),
        "repatriation_ticket": benefits.get("Repatriation Ticket", "N/A"),
        "health_insurance": benefits.get("Health Insurance", "N/A"),
        "annual_leave": benefits.get("Annual Leave", "N/A"),
    }

    def generate_contract(data):
        template_path = "/mnt/data/Faculty_Offer_Template.docx"
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
