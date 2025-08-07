import streamlit as st
from docx import Document
from io import BytesIO
import json
import datetime

# Load benefits data
@st.cache_data
def load_benefits():
    with open("benefits_by_profile.json", "r") as f:
        return json.load(f)

benefits_data = load_benefits()

# UI Inputs
st.title("📄 Faculty Contract Generator")
st.markdown("Automatically generates contract with benefits based on role, campus, and marital status.")

with st.form("contract_form"):
    candidate_id = st.text_input("Candidate ID")
    candidate_name = st.text_input("Candidate Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    designation = st.selectbox("Designation (Rank)", ["Professor", "Senior Instructor"])
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    campus = st.selectbox("Campus", ["Al Ain", "AD/Dubai"])
    college = st.text_input("College or Department")
    reporting_manager = st.text_input("Reporting Manager")
    salary = st.text_input("Monthly Salary (AED)")
    probation_period = st.text_input("Probation Period (in months)", value="6")
    is_international = st.checkbox("International Hire", value=True)
    submitted = st.form_submit_button("Generate Contract")

    if submitted:
        profile_key = f"{designation}|{campus}|{marital_status}"
        benefits = benefits_data.get(profile_key, {})

        # Load the contract template
        template_path = "Faculty_Offer_Template.docx"
        doc = Document(template_path)

        # Replace placeholders
        placeholders = {
            "{{salutation}}": f"{designation} {candidate_name}",
            "{{candidate_id}}": candidate_id,
            "{{phone}}": phone,
            "{{email}}": email,
            "{{designation}}": designation,
            "{{position_title}}": college,
            "{{reporting_manager}}": reporting_manager,
            "{{salary}}": salary,
            "{{probation_period}}": probation_period,
            "{{housing_allowance}}": str(benefits.get("housing_allowance", "")),
            "{{furniture_allowance}}": str(benefits.get("furniture_allowance", "")),
            "{{school_allowance}}": str(benefits.get("school_allowance", "")),
            "{{annual_leave}}": str(benefits.get("annual_leave_days", "")),
            "{{relocation_allowance}}": str(benefits.get("relocation_allowance", "")),
            "{{repatriation_allowance}}": str(benefits.get("repatriation_allowance", "")),
            "{{joining_ticket}}": benefits.get("joining_ticket", ""),
            "{{health_insurance}}": benefits.get("health_insurance", ""),
            "{{tuition_employee}}": benefits.get("tuition_waiver", {}).get("employee", ""),
            "{{tuition_dependent}}": benefits.get("tuition_waiver", {}).get("dependent", ""),
            "{{tuition_family}}": benefits.get("tuition_waiver", {}).get("family", ""),
            "{{joining_ticket_if}}": benefits.get("joining_ticket", "") if is_international else "N/A",
            "{{contract_date}}": datetime.datetime.today().strftime('%d %B %Y')
        }

        for p in doc.paragraphs:
            for key, value in placeholders.items():
                if key in p.text:
                    inline = p.runs
                    for i in range(len(inline)):
                        if key in inline[i].text:
                            inline[i].text = inline[i].text.replace(key, str(value))

        # Save to buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("Contract generated successfully!")
        st.download_button(
            label="📥 Download Contract",
            data=buffer,
            file_name=f"Contract_{candidate_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


