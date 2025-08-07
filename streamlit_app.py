import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import datetime
import os
from io import BytesIO

st.set_page_config(page_title="ADU Contract Generator", layout="centered")
st.title("📄 ADU Contract Generator")

# --- Upload the ADU Logo ---
st.subheader("1. Upload ADU Logo (optional)")
logo_file = st.file_uploader("Upload ADU logo (image)", type=["png", "jpg", "jpeg"])

# --- Select Employment Offer Type ---
st.subheader("2. Select Employment Offer Type")
offer_types = {
    "Assistant Professor (AA, Married)": "Faculty_AssistantProfessor_AA_Married_Expat.docx",
    "Associate/Full Professor (AD, Married)": "Faculty_AssociateOrFullProfessor_AD_Married_Expat.docx",
    "Instructor (AD, Single)": "Faculty_Instructor_AD_Single_Expat.docx",
    "Staff (Emirati)": "Staff_General_AD_Emirati.docx",
    "Staff (Expat)": "Staff_General_AD_Expat.docx",
    "Visiting Faculty – One Semester": "Faculty_Visiting_AssistantProfessor_AlAin.docx"
}
selected_offer = st.selectbox("Choose Offer Type", list(offer_types.keys()))

# --- Input Fields ---
st.subheader("3. Fill in Candidate Information")
ref_id = st.text_input("Reference ID (Ref:)")
date = st.date_input("Date", datetime.date.today())
candidate_name = st.text_input("Candidate Full Name")
tel = st.text_input("Telephone Number")
email = st.text_input("Email Address")
designation = st.selectbox("Salutation", ["Dr.", "Mr.", "Ms.", "Mrs."])
position_title = st.text_input("Position Title")
manager = st.text_input("Reports To (Chair/Dean/Manager)")
salary = st.text_input("Total Monthly Salary (AED)")
hire_type = st.selectbox("Hire Type", ["Local", "International"])

# --- Generate Contract ---
st.subheader("4. Generate Offer Letter")
if st.button("Generate Contract"):
    try:
        template_path = os.path.join("templates", offer_types[selected_offer])
        doc = DocxTemplate(template_path)

        context = {
            "REF": ref_id,
            "DATE": date.strftime("%d %B %Y"),
            "NAME": candidate_name,
            "TEL": tel,
            "EMAIL": email,
            "SALUTATION": designation,
            "POSITION_TITLE": position_title,
            "MANAGER": manager,
            "SALARY": salary,
            "HIRE_TYPE": hire_type,
        }

        if logo_file is not None:
            image_stream = BytesIO(logo_file.read())
            context["LOGO"] = InlineImage(doc, image_stream, width=Mm(40))
        else:
            context["LOGO"] = ""

        doc.render(context)
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        st.success("✅ Contract generated successfully!")
        st.download_button(
            label="📥 Download Contract (DOCX)",
            data=output,
            file_name=f"{candidate_name.replace(' ', '_')}_Contract.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"❌ Failed to generate contract: {e}")
