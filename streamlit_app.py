import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import tempfile
import base64
import zipfile
import datetime

# --- Helpers ---
def determine_title(degree, gender):
    degree = str(degree).lower()
    gender = str(gender).lower()
    if "phd" in degree or "dphil" in degree or "doctorate" in degree:
        return "Dr."
    elif gender == "female":
        return "Ms."
    else:
        return "Mr."

def set_cell_background(cell, color="D9D9D9"):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    shd.set(qn('w:val'), "clear")
    shd.set(qn('w:color'), "auto")
    tcPr.append(shd)

def add_centered_logo(doc, logo_path):
    header = doc.sections[0].header
    paragraph = header.paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(logo_path, width=Inches(1.5))
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

# --- Contract Generator ---
def generate_contracts(df, logo_file):
    output_paths = []
    temp_dir = tempfile.mkdtemp()
    today_date = datetime.date.today().strftime("%d %B %Y")

    logo_temp_path = None
    if logo_file:
        logo_temp_path = os.path.join(temp_dir, "logo.png")
        with open(logo_temp_path, "wb") as f:
            f.write(logo_file.read())

    for i in range(len(df)):
        row = df.iloc[i]
        doc = Document()

        # Centered logo
        if logo_temp_path:
            add_centered_logo(doc, logo_temp_path)

        # Heading 1 – SERVICE AGREEMENT
        heading = doc.add_heading('SERVICE AGREEMENT', level=1)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for run in heading.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Date
        date_para = doc.add_paragraph(f"This Agreement is made on: {today_date}")
        for run in date_para.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0, 0, 0)
        date_para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        # Sections
        def add_section_header(text):
            table = doc.add_table(rows=1, cols=1)
            cell = table.rows[0].cells[0]
            cell.text = text
            set_cell_background(cell)
            for run in cell.paragraphs[0].runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
                run.font.bold = True
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        def add_paragraph(text):
            para = doc.add_paragraph(text)
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
            para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        title = determine_title(row['Degree'], row['Gender'])
        faculty_name = f"{title} {row['Name']}"

        # Opening Statement
        add_section_header("Opening Statement:")
        add_paragraph(
            "This Service Agreement is entered into between Abu Dhabi University (hereinafter referred to as the “First Party”) "
            "and the employee identified below (hereinafter referred to as the “Second Party”). This Agreement outlines the terms "
            "and conditions under which the Second Party will perform academic duties for the specified academic period."
        )

        # Parties
        add_section_header("Parties:")
        add_paragraph(
            f"First Party: Abu Dhabi University\n"
            f"Second Party:\n• Name: {faculty_name}\n• Faculty Type: {row['Faculty Type']}\n"
            f"• College/Department: {row['College/Department']}\n• Faculty ID: {row.get('Faculty ID', 'N/A')}"
        )

        # Contract Period
        add_section_header("Contract Period:")
        add_paragraph(f"Academic Year: AY {row['Academic Year']}\nSemester / Term: {row['Semester/Term']}")

        # Scope of Work
        add_section_header("Scope of Work:")
        bullet_points = [
            "Deliver the assigned course(s) in line with the approved schedule and syllabus.",
            "Submit final student grades in accordance with the official academic calendar.",
            "Complete and upload all required course documentation (e.g., course files, assessment materials).",
            "Remain available to address student inquiries, including during any approved post-semester extension period."
        ]
        for point in bullet_points:
            para = doc.add_paragraph(point, style='List Bullet')
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
            para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        # Compensation
        add_section_header("Compensation")
        add_paragraph(f"Total Compensation (AED): {row['Compensation (AED)']}")

        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        headers = ['Workload Hours', 'Course Level', 'Payment Details', 'Compensation (AED)']
        values = [
            str(row['Workload Hours']),
            row['Course Level'],
            row['Payment Details'],
            str(row['Compensation (AED)'])
        ]
        for idx, h in enumerate(headers):
            cell = table.rows[0].cells[idx]
            cell.text = h
            for run in cell.paragraphs[0].runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        row_cells = table.add_row().cells
        for idx, val in enumerate(values):
            row_cells[idx].text = val
            for run in row_cells[idx].paragraphs[0].runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
            row_cells[idx].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Instalments
        add_section_header("Instalment Details:")
        instalments = [
            "• The total compensation will be paid in equal monthly instalments over the duration of the contract, with each instalment released upon completion of teaching duties and submission of required deliverables (e.g., grades and course files).",
            "• Instalment payments are conditional upon adherence to Abu Dhabi University’s academic policies and timelines. Any failure to meet contractual obligations may result in payment delays, adjustments, or withholdings."
        ]
        for line in instalments:
            add_paragraph(line)

        # Policies
        add_section_header("Policies and Compliance")
        policies = [
            "Comply with all applicable Abu Dhabi University policies, procedures, and academic regulations.",
            "Demonstrate professionalism and ethical conduct in all teaching-related activities.",
            "Support institutional quality assurance, accreditation, and review processes as requested."
        ]
        for point in policies:
            para = doc.add_paragraph(point, style='List Bullet')
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0, 0, 0)
            para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        # Signatures
        add_section_header("Signatures and Acknowledgement")
        add_paragraph("By signing this Agreement, all parties confirm their understanding and acceptance of the terms set forth herein.")

        sign_table = doc.add_table(rows=4, cols=4)
        sign_table.style = 'Table Grid'
        labels = ['Name', 'Title', 'Signature', 'Date']
        for i in range(4):
            cell = sign_table.cell(0, i)
            cell.text = labels[i]
            for run in cell.paragraphs[0].runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)

        sign_table.cell(1, 0).text = str(row.get('Dean Name', ''))
        sign_table.cell(1, 1).text = 'Dean / Department Head / Authorized Signatory'
        sign_table.cell(2, 0).text = str(row.get('Faculty Name', ''))
        sign_table.cell(2, 1).text = 'Faculty – Second Party'
        sign_table.cell(3, 0).text = str(row.get('HR Representative Name', ''))
        sign_table.cell(3, 1).text = 'Representative, Talent Empowerment and Growth Department'

        for r in range(1, 4):
            for c in range(4):
                for run in sign_table.cell(r, c).paragraphs[0].runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(0, 0, 0)

        filename = f"{faculty_name.replace(' ', '_')}_{row['Academic Year'].replace('/', '-')}_{row['Semester/Term'].replace(' ', '_')}.docx"
        path = os.path.join(temp_dir, filename)
        doc.save(path)
        output_paths.append(path)

    return output_paths

# --- Streamlit Interface ---
st.set_page_config(layout="centered")
st.title("📄 ADU Faculty Contract Generator")
st.markdown("Upload Excel file & logo to generate professional contracts.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
logo_file = st.file_uploader("Upload ADU Logo (PNG)", type=["png"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Excel loaded.")

        if st.button("Generate Contracts"):
            with st.spinner("Generating..."):
                paths = generate_contracts(df, logo_file)

            zip_path = os.path.join(tempfile.gettempdir(), "All_Contracts.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for p in paths:
                    zipf.write(p, arcname=os.path.basename(p))

            with open(zip_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<a href="data:application/zip;base64,{b64}" download="All_Contracts.zip">📦 Download All Contracts (ZIP)</a>', unsafe_allow_html=True)

            for p in paths:
                with open(p, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    fname = os.path.basename(p)
                    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{fname}">📄 Download {fname}</a>', unsafe_allow_html=True)

            st.success("✅ All contracts ready.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
