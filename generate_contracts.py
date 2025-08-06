import pandas as pd
from docx import Document
from docx.shared import Inches
import os

def determine_title(degree, gender):
    degree = str(degree).lower()
    gender = str(gender).lower()
    if "phd" in degree or "dphil" in degree or "doctorate" in degree:
        return "Dr."
    elif gender == "female":
        return "Ms."
    else:
        return "Mr."

def generate_contracts(excel_path, output_dir):
    df = pd.read_excel(excel_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for _, row in df.iterrows():
        doc = Document()

        try:
            doc.add_picture('adu_logo.png', width=Inches(1.5))
        except:
            pass

        doc.add_heading('SERVICE AGREEMENT', 0)
        doc.add_paragraph('This Agreement is made on: [Insert Date]')

        title = determine_title(row['Degree'], row['Gender'])
        faculty_name = f"{title} {row['Name']}"

        doc.add_paragraph(
            "This Service Agreement is entered into between Abu Dhabi University (hereinafter referred to as the “First Party”) "
            "and the employee identified below (hereinafter referred to as the “Second Party”). This Agreement outlines the terms and "
            "conditions under which the Second Party will perform academic duties for the specified academic period."
        )

        doc.add_heading("Parties:", level=1)
        doc.add_paragraph("First Party: Abu Dhabi University")
        doc.add_paragraph(
            f"Second Party:\n"
            f"• Name: {faculty_name}\n"
            f"• Faculty Type: {row['Faculty Type']}\n"
            f"• College/Department: {row['College/Department']}\n"
            f"• Faculty ID: {row.get('Faculty ID', 'N/A')}"
        )

        doc.add_heading("Contract Period:", level=1)
        doc.add_paragraph(f"Academic Year: AY {row['Academic Year']}\nSemester / Term: {row['Semester/Term']}")

        doc.add_heading("Scope of Work:", level=1)
        scope = [
            "Deliver the assigned course(s) in line with the approved schedule and syllabus.",
            "Submit final student grades in accordance with the official academic calendar.",
            "Complete and upload all required course documentation (e.g., course files, assessment materials).",
            "Remain available to address student inquiries, including during any approved post-semester extension period."
        ]
        for point in scope:
            doc.add_paragraph(point, style='List Bullet')

        doc.add_heading("Compensation", level=1)
        doc.add_paragraph(f"Total Compensation (AED): {row['Compensation (AED)']}")

        table = doc.add_table(rows=1, cols=4)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Workload Hours'
        hdr_cells[1].text = 'Course Level'
        hdr_cells[2].text = 'Payment Details'
        hdr_cells[3].text = 'Compensation (AED)'

        row_cells = table.add_row().cells
        row_cells[0].text = str(row['Workload Hours'])
        row_cells[1].text = row['Course Level']
        row_cells[2].text = row['Payment Details']
        row_cells[3].text = str(row['Compensation (AED)'])

        doc.add_heading("Instalment Details:", level=1)
        doc.add_paragraph("• The total compensation will be paid in equal monthly instalments over the duration of the contract.")
        doc.add_paragraph("• Instalment payments are conditional upon adherence to Abu Dhabi University policies.")

        doc.add_heading("Policies and Compliance", level=1)
        compliance = [
            "Comply with all applicable Abu Dhabi University policies and academic regulations.",
            "Demonstrate professionalism and ethical conduct in all teaching-related activities.",
            "Support quality assurance, accreditation, and review processes as requested."
        ]
        for point in compliance:
            doc.add_paragraph(point, style='List Bullet')

        doc.add_heading("Signatures and Acknowledgement", level=1)
        doc.add_paragraph("By signing this Agreement, all parties confirm understanding and acceptance of the terms set forth.")

        sign_table = doc.add_table(rows=4, cols=4)
        sign_table.style = 'Table Grid'
        sign_table.cell(0, 0).text = 'Name'
        sign_table.cell(0, 1).text = 'Title'
        sign_table.cell(0, 2).text = 'Signature'
        sign_table.cell(0, 3).text = 'Date'

        sign_table.cell(1, 0).text = row['Dean Name']
        sign_table.cell(1, 1).text = 'Dean / Authorized Signatory'
        sign_table.cell(2, 0).text = row['Faculty Name']
        sign_table.cell(2, 1).text = 'Faculty – Second Party'
        sign_table.cell(3, 0).text = row['HR Representative Name']
        sign_table.cell(3, 1).text = 'Representative, HR Department'

        filename = f"{faculty_name.replace(' ', '_')}_{row['Academic Year'].replace('/', '-')}_{row['Semester/Term'].replace(' ', '_')}.docx"
        doc.save(os.path.join(output_dir, filename))

    return f"Contracts successfully generated in {output_dir}"
