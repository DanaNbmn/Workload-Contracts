import streamlit as st
from docx import Document
from io import BytesIO
from datetime import date

# --- Helper Function ---
def fill_template(template_path, data):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, val in data.items():
            if f"{{{{{key}}}}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if f"{{{{{key}}}}}" in inline[i].text:
                        inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(val))
    return doc

# --- Streamlit UI ---
st.set_page_config(page_title="ADU Contract Generator", page_icon="📄")
st.title("📄 Abu Dhabi University Contract Generator")
st.markdown("Fill in the employee details below to generate a professional faculty offer letter.")

# --- Form ---
with st.form("contract_form"):
    col1, col2 = st.columns(2)
    with col1:
        employee_id = st.text_input("Employee ID")
        name = st.text_input("Full Name")
        designation = st.selectbox("Salutation", ["Dr.", "Mr.", "Ms.", "Mrs."])
        position_title = st.text_input("Position Title")
        salary = st.text_input("Total Monthly Salary (AED)")
        probation_period = st.selectbox("Probation Period (months)", [3, 6, 9])
        repatriation_allowance = st.selectbox("Repatriation Allowance (AED)", [2000, 3000])
    with col2:
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        college_or_department = st.text_input("College or Department")
        reporting_manager = st.text_input("Reporting Manager")
        campus = st.selectbox("Campus", ["Al Ain", "Abu Dhabi", "Dubai"])
        marital_status = st.selectbox("Marital Status", ["Married", "Single"])
        international_hire = st.selectbox("International Hire?", ["Joining", ""])

    st.divider()
    st.markdown("### 🎁 Benefits Input")
    col3, col4 = st.columns(2)
    with col3:
        housing_allowance = st.text_input("Housing Allowance (AED)", "45000")
        furniture_allowance = st.text_input("Furniture Allowance (AED)", "30000")
        education_allowance = st.text_input("Education Allowance (AED)", "50000")
    with col4:
        annual_leave_days = st.selectbox("Annual Leave Days", [42, 56])
        today = date.today().strftime("%d/%m/%Y")

    submitted = st.form_submit_button("Generate Contract")

# --- Generate and Download ---
if submitted:
    data = {
        "employee_id": employee_id,
        "date": today,
        "name": name,
        "designation": designation,
        "position_title": position_title,
        "college_or_department": college_or_department,
        "campus": campus,
        "reporting_manager": reporting_manager,
        "salary": salary,
        "phone": phone,
        "email": email,
        "probation_period": probation_period,
        "housing_allowance": housing_allowance,
        "furniture_allowance": furniture_allowance,
        "repatriation_allowance": repatriation_allowance,
        "annual_leave_days": annual_leave_days,
        "education_allowance": education_allowance,
        "international_joining": international_hire,
    }

    doc = fill_template("Updated_Faculty_Offer_Template.docx", data)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.success("✅ Contract generated successfully!")
    st.download_button(
        label="📥 Download Contract (.docx)",
        data=buffer,
        file_name=f"Contract_{employee_id}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
