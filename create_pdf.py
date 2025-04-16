from fpdf import FPDF

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Read content from text file
    with open("pdf files/sample_telecom_doc.txt", "r") as file:
        content = file.readlines()
    
    # Add content to PDF
    for line in content:
        pdf.cell(200, 10, txt=line.strip(), ln=True)
    
    # Save the PDF
    pdf.output("pdf files/sample_telecom_doc.pdf")
    
    print("Sample PDF created successfully!")

if __name__ == "__main__":
    create_sample_pdf()
