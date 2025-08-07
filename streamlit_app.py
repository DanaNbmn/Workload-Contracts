from docx import Document
from docx.shared import Inches
from docx.enum.section import WD_SECTION

# Recreate the Word document
doc = Document()

# Set margins
section = doc.sections[0]
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)

# Add logo to header
header = section.header
header_paragraph = header.paragraphs[0]
run = header_paragraph.add_run()
run.add_picture("/mnt/data/Logo.png", width=Inches(1.2))

# Add footer with wide banner image
footer = section.footer
footer_paragraph = footer.paragraphs[0]
footer_paragraph.alignment = 1  # Center
run = footer_paragraph.add_run()
run.add_picture("/mnt/data/08137723-09f6-4a2c-808f-98a34237e62b.png", width=Inches(6.5))

# Add contract body with placeholders
doc.add_paragraph("Ref: TEG/{{Employee_ID}}")
doc.add_paragraph("Date: {{Offer_Date}}")
doc.add_paragraph("{{Candidate_Name}}\nTel no: {{Candidate_Phone}}\nEmail ID: {{Candidate_Email}}")

doc.add_paragraph("""
Dear Dr.,

Abu Dhabi University (ADU) is pleased to offer you a contract of employment for an Assistant Professor in {{Position_Title}} position in the {{College_Name}} based in {{Campus_Location}}, UAE. This position reports to the Dean/Chair of {{Department_Name}}. Your first day of employment with the Abu Dhabi University will be based on the availability of legal approvals and the term of your contract shall be limited to a period of two years, renewable upon mutual agreement.
""")

doc.add_paragraph("1. Package:")
doc.add_paragraph("Your total monthly compensation will be AED {{Total_Compensation}}. In addition, the following terms, conditions and benefits apply:")
doc.add_paragraph("1.1. Basic Salary (50%) and Other Allowance (50%) paid at the end of each calendar month.")
doc.add_paragraph("1.2. The first 6 (six) months period from the start date shall be deemed to be the Probationary Period.")
doc.add_paragraph("1.3. Housing Allowance: A housing allowance of AED {{Housing_Allowance}} per annum will be provided if university accommodation is not available.")
doc.add_paragraph("1.4. Furniture Allowance: {{Furniture_Allowance_Clause}}")
doc.add_paragraph("1.5. Annual Leave Tickets: Cash in lieu of economy class air tickets for you, spouse, and up to 2 children under 21 years residing in the UAE.")
doc.add_paragraph("1.6. Joining and Repatriation Tickets: Economy class air tickets for you and your eligible dependents upon commencement and repatriation.")
doc.add_paragraph("1.7. Relocation and Repatriation Allowance: AED 3,000 each for relocation and repatriation, reimbursed based on receipts.")
doc.add_paragraph("1.8. Medical Insurance: Provided for you, your spouse, and up to 3 dependent children under 21 years of age.")
doc.add_paragraph("1.9. Annual Leave: 56 calendar days of paid leave per academic year.")
doc.add_paragraph("1.10. Tuition Fees Subsidy: AED 25,000 per eligible child (up to AED 50,000 per family) for UAE-based schooling.")
doc.add_paragraph("1.11. ADU Tuition Waiver: 75% for self, 50% for dependents, 25% for immediate family, post one year of service.")
doc.add_paragraph("1.12. End of Service Gratuity: One month’s basic salary per year of service, pro-rated (minimum one year of service required).")

# Save final document
file_path = "/mnt/data/Faculty_Offer_Letter_Template_Final_Footer.docx"
doc.save(file_path)
file_path
