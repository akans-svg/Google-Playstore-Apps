from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Google Play Store Analytics Report', 0, 1, 'C')
        self.ln(10)

def generate_pdf(df, figures_dict):
    """
    Saves plots as temp images, puts them in PDF, then returns PDF bytes.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # 1. Summary Statistics Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '1. Executive Summary', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    summary_text = [
        f"Total Apps Analyzed: {len(df)}",
        f"Average Rating: {df['Rating'].mean():.2f}",
        f"Total Installs (Approx): {df['Installs'].sum():,.0f}",
        f"Most Expensive App: ${df['Price'].max()}"
    ]
    
    for line in summary_text:
        pdf.cell(0, 8, line, 0, 1)
    
    pdf.ln(10)

    # 2. Visualizations Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Visualizations', 0, 1)
    
    # Save figures temporarily to add to PDF
    for title, fig in figures_dict.items():
        img_path = f"temp_{title}.png"
        fig.savefig(img_path, dpi=150) # Save temp image
        
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, title, 0, 1)
        pdf.image(img_path, w=170) # Add image to PDF
        pdf.ln(5)
        
        os.remove(img_path) # Clean up temp file

    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')