import streamlit as st
from docx import Document
import datetime
import os

# --- Clause Functions ---
def get_furniture_clause(rank, marital, campus):
    if rank in ["Professor", "Associate Professor", "Assistant Professor"]:
        if campus == "Abu Dhabi":
            return f"A furniture allowance of AED {'30,000' if marital == 'Married' else '20,000'} will be provided at the start of your employment. This is a forgivable loan amortized over three years."
        else:
            return f"A furniture allowance of AED {'25,000' if marital == 'Married' else '15,000'} will be provided at the start of your employment. This is a forgivable loan amortized over three years."
    else:
        return f"A furniture allowance of AED {'15,000' if marital == 'Married' else '12,000'} will be provided at the start of your employment. This is a forgivable loan amortized over three years."

def get_housing_clause(rank, marital):
    if rank in ["Professor", "Associate Professor", "Assistant Professor"]:
        return f"A housing allowance of AED {'60,000' if marital == 'Married' else '45,000'} per annum will be provided if university accommodation is not available."
    else:
        return f"A housing allowance of AED {'45,000' if marital == 'Married' else '35,000'} per annum will be provided if university accommodation is not available."

def get_children_school_clause(marital):
    if marital == "Married":
        return "A school tuition subsidy of AED 20,000 per eligible child (up to AED 50,000 per family) will be provided."
    return "Not applicable."

def get_relocation_clause(rank, hire_type):
    if hire_type == "International":
        amount = "3,000" if rank not in ["Senior Instructor", "Instructor"] else "2,000"
        return f"Relocation and repatriation allowance of AED {amount} plus Economy Class air tickets for self, spouse, and up to two children under 21."
    return "Not applicable."

def get_leave_clause(rank):
    return "You will be entitled to 56 calendar days of paid annual leave." if rank in ["Professor", "Associate Professor", "Assistant Professor"] else "You will be entitled to 42 calendar days of paid annual leave."

def get_insurance_clause():
    return "Medical insurance coverage for self, spouse, and up to three children under 21 residing in the UAE."

def get_ticket_cash_clause():
    return "Annual leave ticket cash allowance in lieu of air tickets for self, spouse, and two eligible children."

def get_joining_ticket_clause():
    return "Economy Class tickets for self, spouse, and two eligible children upon joining and repatriation."

def get_tuition_waiver_clause():
    return "75% tuition waiver for self, 50% for dependents, and 25% for immediate family as per ADU policy (after 1 year of service)."

def get_end_of_service_clause():
    return "End of service gratuity of one month's basic salary per year of service, pro-rated. Not applicable for service less than one year."

# --- Streamlit App ---
st.set_page_config(page_title="Faculty Contract Generator", layout="centered")
st.title("📄 Faculty Contract Generator - Abu Dhabi University")

with st.form("faculty_form"):
    st.subheader("Enter Faculty Details")

    employee_id = st.text_input("Employee ID")
    candidate_name = st.text_input("Candidate Name")
    candidate_last_name = st.text_input("Candidate Last Name")
    faculty_rank = st.selectbox("Faculty Rank", ["Professor", "Associate Professor", "Assistant Professor", "Senior Instructor", "Instructor"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])
    campus = st.selectbox("Campus", ["Abu Dhabi", "Al Ain", "Dubai"])
    department = st.text_input("Department / College")
    supervisor = st.text_input("Dean/Chair Name")
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    hire_type = st.selectbox("Hire Type", ["Local", "International"])
    monthly_salary = st.text_input("Total Monthly Compensation (AED)", placeholder="e.g. 25000")

    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    doc = Document("Faculty_Offer_Letter_Template_Final_Footer.docx")
    today = datetime.date.today().strftime("%d %B %Y")

    # Replacement dictionary
    replacements = {
        "{{Employee_ID}}": employee_id,
        "{{Date}}": today,
        "{{Candidate_Name}}": candidate_name,
        "{{Candidate_Last_Name}}": candidate_last_name,
        "{{Phone_Number}}": phone_number,
        "{{Email}}": email,
        "{{Position_Title}}": faculty_rank,
        "{{Campus}}": campus,
        "{{Department}}": department,
        "{{Supervisor_Name}}": supervisor,
        "{{Monthly_Salary}}": monthly_salary,
        "{{Furniture_Allowance_Clause}}": get_furniture_clause(faculty_rank, marital_status, campus),
        "{{Housing_Allowance_Clause}}": get_housing_clause(faculty_rank, marital_status),
        "{{Children_School_Allowance_Clause}}": get_children_school_clause(marital_status),
        "{{Relocation_Repatriation_Clause}}": get_relocation_clause(faculty_rank, hire_type),
        "{{Annual_Leave_Clause}}": get_leave_clause(faculty_rank),
        "{{Medical_Insurance_Clause}}": get_insurance_clause(),
        "{{Annual_Ticket_Cash_Allowance_Clause}}": get_ticket_cash_clause(),
        "{{Joining_Repatriation_Ticket_Clause}}": get_joining_ticket_clause(),
        "{{Tuition_Waiver_Clause}}": get_tuition_waiver_clause(),
        "{{End_of_Service_Clause}}": get_end_of_service_clause(),
    }

    for paragraph in doc.paragraphs:
        for placeholder, value in replacements.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    output_filename = f"{employee_id}_{candidate_name.replace(' ', '_')}_Offer_Letter.docx"
    doc.save(output_filename)

    with open(output_filename, "rb") as file:
        st.success("✅ Offer Letter Generated!")
        st.download_button(label="📥 Download Contract", data=file, file_name=output_filename)
