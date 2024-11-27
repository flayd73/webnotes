# scripts/generate_pdf.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os

def generate_pdf(summary, output_path):
    # Define page size and margins
    page_width, page_height = letter
    margin = 0.5 * inch
    text_width = page_width - 2 * margin
    text_height = page_height - 2 * margin

    # Create a PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = ParagraphStyle(name='Title', parent=normal_style, fontSize=14, leading=16, alignment=1)  # Centered title

    # Add title
    title = os.path.basename(output_path).replace(".pdf", "")
    title_paragraph = Paragraph(title, title_style)
    elements.append(title_paragraph)

    # Add a line break
    elements.append(Paragraph("<br/>", normal_style))

    # Add summary text with wrapping
    summary_paragraph = Paragraph(summary, normal_style)
    elements.append(summary_paragraph)

    # Build the document
    doc.build(elements)
