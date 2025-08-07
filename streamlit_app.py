# Prepare the Streamlit app code as a downloadable .py file
streamlit_code = '''
import streamlit as st
from docx import Document
import datetime
import base64
from io import BytesIO

st.title("Faculty Offer Letter Generator")

# User inputs
candidate_name = st.text_input("Candidate Name")
candidate_email = st.text_input("Candidate Email")
candidate_phone = st.text_input("Candidate Phone")
employee_id = st.text_input("Employee ID")
position_title = st.text_input("Position Title")
college_name = st.text_input("College Name")
department_name = st.text_input("Department Name")
campus_location = st.selectbox("Campus Location", ["Abu Dhabi", "Al Ain"])
offer_date = st.date_input("Offer Date", value=datetime.date.today())
total_compensation = st.text_input("Total Compensation (AED)")
housing_allowance = st.text_input("Housing Allowance (AED)")
furniture_allowance_clause = st.text_area("Furniture Allowance Clause")

# Load and fill Word template
def generate_contract():
    doc = Document("Faculty_Offer_Letter_Template_Final_Footer.docx")
    for p in doc.paragraphs:
        inline_replace(p, {
            "{{Candidate_Name}}": candidate_name,
            "{{Candidate_Email}}": candidate_email,
            "{{Candidate_Phone}}": candidate_phone,
            "{{Employee_ID}}": employee_id,
            "{{Position_Title}}": position_title,
            "{{College_Name}}": college_name,
            "{{Department_Name}}": department_name,
            "{{Campus_Location}}": campus_location,
            "{{Offer_Date}}": offer_date.strftime("%d-%m-%Y"),
            "{{Total_Compensation}}": total_compensation,
            "{{Housing_Allowance}}": housing_allowance,
            "{{Furniture_Allowance_Clause}}": furniture_allowance_clause
        })
    return doc

def inline_replace(paragraph, replacements):
    for key, val in replacements.items():
        if key in paragraph.text:
            inline = paragraph.runs
            for i in range(len(inline)):
                if key in inline[i].text:
                    inline[i].text = inline[i].text.replace(key, val)

# Generate and download button
if st.button("Generate Contract"):
    final_doc = generate_contract()
    buffer = BytesIO()
    final_doc.save(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Faculty_Offer_Letter.docx">📄 Download Offer Letter</a>'
    st.markdown(href, unsafe_allow_html=True)
'''

# Save the code to a Python file
streamlit_file_path = "/mnt/data/faculty_contract_generator_app.py"
with open(streamlit_file_path, "w") as f:
    f.write(streamlit_code)

streamlit_file_path
