import streamlit as st
from docx import Document
from io import BytesIO
import datetime

TEMPLATE_PATH = "Faculty_Offer_Letter_Template_Final_Format.docx"

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

def determine_furniture_allowance(campus, rank, marital_status):
    if campus == "Al Ain" and marital_status == "Married":
        return "AED 30,000"
    elif rank == "Professor":
        return "AED 25,000"
    else:
        return "AED 20,000"

st.title("📄 Faculty Offer Letter Generator")

with st.form("offer_form"):
    candidate_id = st.text_input("Candidate ID")
    candidate_name = st.text_input("Candidate Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    position = st.text_input("Position Title")
    department = st.text_input("Department")
    reports_to = st.text_input("Reports To")
    total_comp = st.text_input("Total Monthly Compensation (AED)", "15000")
    campus = st.selectbox("Campus", ["Abu Dhabi", "Al Ain", "Other"])
    rank = st.selectbox("Faculty Rank", ["Assistant Professor", "Associate Professor", "Professor"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])
    date_today = st.date_input("Contract Date", value=datetime.date.today())
    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    furniture_allowance = determine_furniture_allowance(campus, rank, marital_status)

    fields = {
        "Candidate_ID": candidate_id,
        "Candidate_Name": candidate_name,
        "Phone_Number": phone,
        "Email": email,
        "Position": position,
        "Department": department,
        "Reports_To": reports_to,
        "Total_Compensation": total_comp,
        "Date": date_today.strftime("%d %B %Y"),
        "Furniture_Allowance": furniture_allowance
    }

    try:
        final_doc = generate_contract(fields)
        buffer = BytesIO()
        final_doc.save(buffer)
        buffer.seek(0)

        st.success("✅ Contract generated successfully!")
        st.download_button(
            label="📄 Download Offer Letter",
            data=buffer,
            file_name=f"Offer_Letter_{candidate_name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"❌ Error generating contract: {str(e)}")
