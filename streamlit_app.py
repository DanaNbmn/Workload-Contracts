import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os
import tempfile
import base64
import zipfile
import datetime

# --- Helper: Determine Title Prefix ---
def determine_title(degree, gender):
    degree = str(degree).lower()
    gender = str(gender).lower()
    if "phd" in degree or "dphil" in degree or "doctorate" in degree:
        return "Dr."
    elif gender == "female":
        return "Ms."
    else:
        return "Mr."

# --- Insert Logo Centered in Header ---
def add_centered_logo(section, logo_path):
    header = section.header
    paragraph = header.paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(logo_path, width=Inches(1.5))
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

# --- Format Entire Document Consistently ---
def format_paragraph(paragraph, font_size=10, bold=False):
    for run in paragraph.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(0, 0, 0)
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

# --- Contract Generator Function ---
def generate_contracts(df, logo_file):
    output_paths = []
    temp_dir = tempfile.mkdtemp()
    today_date = datetime.date.today().strftime("%d %B %Y")

    logo_temp = None
    if logo_file:
        logo_temp = os.path.join(temp_dir, "logo.png")
        with open(logo_temp, "wb") as f:
            f.write(logo_file.read())

    for i in range(len(df)):
        row = df.iloc[i]
        doc = Document()

        section = doc.sections[0]
        if logo_temp:
            add_centered_logo(section, logo_temp)

        # Heading
        heading = doc.add_heading('SERVICE AGREEMENT', level=1)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for run in heading.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Insert date
        date_para = doc.add_paragraph(f"This Agreement is made on: {today_date}")
        format_paragraph(date_para)

        # Opening Statement
        doc.add_heading("Opening Statement:", level=2)
        para = doc.add_paragraph(
            "This Service Agreement is entered into between Abu Dhabi University (hereinafter referred to as the “First Party”) "
            "and the employee identified below (hereinafter referred to as the “Second Party”). This Agreement outlines the terms "
            "and conditions under which the Second Party will perform academic duties for the specified academic period.")
        format_paragraph(para)

        # Parties
        doc.add_heading("Parties:", level=2)
        title = determine_title(row['Degree'], row['Gender'])
        faculty_name = f"{title} {row['Name']}"
        parties_text = (
            "First Party: Abu Dhabi University\n"
            f"Second Party:\n• Name: {faculty_name}\n• Faculty Type: {row['Faculty Type']}\n"
            f"• College/Department: {row['College/Department']}\n• Faculty ID: {row.get('Faculty ID', 'N/A')}"
        )
        para = doc.add_paragraph(parties_text)
        format_paragraph(para)

        # Contract Period
        doc.add_heading("Contract Period:", level=2)
        para = doc.add_paragraph(f"Academic Year: AY {row['Academic Year']}\nSemester / Term: {row['Semester/Term']}")
        format_paragraph(para)

        # Scope of Work
        doc.add_heading("Scope of Work:", level=2)
        scope_points = [
            "Deliver the assigned course(s) in line with the approved schedule and syllabus.",
            "Submit final student grades in accordance with the official academic calendar.",
            "Complete and upload all required course documentation (e.g., course files, assessment materials).",
            "Remain available to address student inquiries, including during any approved post-semester extension period."
        ]
        for point in scope_points:
            para = doc.add_paragraph(point, style='List Bullet')
            format_paragraph(para)

        # Compensation
        doc.add_heading("Compensation", level=2)
        para = doc.add_paragraph(f"Total Compensation (AED): {row['Compensation (AED)']}")
        format_paragraph(para)

        # Compensation Table
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        headers = ['Workload Hours', 'Course Level', 'Payment Details', 'Compensation (AED)']
        for idx, text in enumerate(headers):
            cell = table.rows[0].cells[idx]
            cell.text = text
            format_paragraph(cell.paragraphs[0], bold=True)
        values = [
            str(row['Workload Hours']),
            row['Course Level'],
            row['Payment Details'],
            str(row['Compensation (AED)'])
        ]
        value_cells = table.add_row().cells
        for idx, text in enumerate(values):
            value_cells[idx].text = text
            format_paragraph(value_cells[idx].paragraphs[0])

        # Instalments
        doc.add_heading("Instalment Details:", level=2)
        inst_points = [
            "• The total compensation will be paid in equal monthly instalments over the duration of the contract, with each instalment released upon completion of teaching duties and submission of required deliverables (e.g., grades and course files).",
            "• Instalment payments are conditional upon adherence to Abu Dhabi University’s academic policies and timelines. Any failure to meet contractual obligations may result in payment delays, adjustments, or withholdings."
        ]
        for inst in inst_points:
            para = doc.add_paragraph(inst)
            format_paragraph(para)

        # Compliance
        doc.add_heading("Policies and Compliance", level=2)
        compliance_points = [
            "Comply with all applicable Abu Dhabi University policies, procedures, and academic regulations.",
            "Demonstrate professionalism and ethical conduct in all teaching-related activities.",
            "Support institutional quality assurance, accreditation, and review processes as requested."
        ]
        for point in compliance_points:
            para = doc.add_paragraph(point, style='List Bullet')
            format_paragraph(para)

        # Signature Section
        doc.add_heading("Signatures and Acknowledgement", level=2)
        para = doc.add_paragraph("By signing this Agreement, all parties confirm their understanding and acceptance of the terms set forth herein.")
        format_paragraph(para)

        sign_table = doc.add_table(rows=4, cols=4)
        sign_table.style = 'Table Grid'
        headers = ['Name', 'Title', 'Signature', 'Date']
        for idx, text in enumerate(headers):
            cell = sign_table.cell(0, idx)
            cell.text = text
            format_paragraph(cell.paragraphs[0], bold=True)

        sign_table.cell(1, 0).text = str(row.get('Dean Name', ''))
        sign_table.cell(1, 1).text = 'Dean / Department Head / Authorized Signatory'

        sign_table.cell(2, 0).text = str(row.get('Faculty Name', ''))
        sign_table.cell(2, 1).text = 'Faculty – Second Party'

        sign_table.cell(3, 0).text = str(row.get('HR Representative Name', ''))
        sign_table.cell(3, 1).text = 'Representative, Talent Empowerment and Growth Department'

        for row_cells in sign_table.rows[1:]:
            for cell in row_cells.cells:
                format_paragraph(cell.paragraphs[0])

        filename = f"{faculty_name.replace(' ', '_')}_{row['Academic Year'].replace('/', '-')}_{row['Semester/Term'].replace(' ', '_')}.docx"
        file_path = os.path.join(temp_dir, filename)
        doc.save(file_path)
        output_paths.append(file_path)

    return output_paths

# --- Streamlit UI ---
st.set_page_config(layout="centered")
st.title("📄 ADU Faculty Contract Generator")
st.markdown("Upload Excel & logo to generate professional contracts.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
logo_file = st.file_uploader("Upload ADU Logo (PNG)", type=["png"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Excel file loaded.")

        if st.button("Generate Contracts"):
            with st.spinner("Generating..."):
                contract_paths = generate_contracts(df, logo_file)

            zip_path = os.path.join(tempfile.gettempdir(), "All_Contracts.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for path in contract_paths:
                    zipf.write(path, arcname=os.path.basename(path))

            with open(zip_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<a href="data:application/zip;base64,{b64}" download="All_Contracts.zip">📦 Download All Contracts (ZIP)</a>', unsafe_allow_html=True)

            for path in contract_paths:
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    filename = os.path.basename(path)
                    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Download {filename}</a>', unsafe_allow_html=True)

            st.success("✅ Contracts ready for download.")

    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
