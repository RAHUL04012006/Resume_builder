from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

def generate_pdf(data):
    """
    Generate a PDF resume using ReportLab
    
    Args:
        data (dict): Dictionary containing all resume data
        
    Returns:
        BytesIO: PDF file as a BytesIO object
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles from scratch to avoid conflicts
    custom_styles = {
        'title': ParagraphStyle(
            name='CustomTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            alignment=1,  # 0=left, 1=center, 2=right
            spaceAfter=12
        ),
        'heading': ParagraphStyle(
            name='CustomHeading',
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=0,
            spaceAfter=8,
            spaceBefore=12
        ),
        'normal': ParagraphStyle(
            name='CustomNormal',
            fontName='Helvetica',
            fontSize=12,
            alignment=0,
            spaceAfter=6
        )
    }
    
    # Title
    elements.append(Paragraph(data['name'], custom_styles['title']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Contact information
    contact_info = f"Email: {data['email']} | Phone: {data['phnum']} | {data['city']}, {data['state']}"
    elements.append(Paragraph(contact_info, custom_styles['normal']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Career Objective
    if data.get('ucareerob'):
        elements.append(Paragraph("Career Objective", custom_styles['heading']))
        elements.append(Paragraph(data['ucareerob'], custom_styles['normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # About
    if data.get('uaboutself'):
        elements.append(Paragraph("About", custom_styles['heading']))
        elements.append(Paragraph(data['uaboutself'], custom_styles['normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Education
    if data.get('education'):
        elements.append(Paragraph("Education", custom_styles['heading']))
        for edu in data['education']:
            if 'course' in edu and 'college' in edu and 'graduation' in edu:
                edu_text = f"<b>{edu['course']}</b> - {edu['college']}, {edu['graduation']}"
                elements.append(Paragraph(edu_text, custom_styles['normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Skills
    if data.get('skills'):
        elements.append(Paragraph("Skills", custom_styles['heading']))
        for skill in data['skills']:
            elements.append(Paragraph(f"• {skill}", custom_styles['normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Achievements
    if data.get('achievements'):
        elements.append(Paragraph("Achievements", custom_styles['heading']))
        for achievement in data['achievements']:
            elements.append(Paragraph(f"• {achievement}", custom_styles['normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Personal Details
    elements.append(Paragraph("Personal Details", custom_styles['heading']))
    elements.append(Paragraph(f"<b>Father's Name:</b> {data['fname']}", custom_styles['normal']))
    elements.append(Paragraph(f"<b>Mother's Name:</b> {data['mname']}", custom_styles['normal']))
    elements.append(Paragraph(f"<b>Date of Birth:</b> {data['dob']}", custom_styles['normal']))
    elements.append(Paragraph(f"<b>Permanent Address:</b> {data['paddress']}", custom_styles['normal']))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value from the BytesIO buffer
    pdf_data = buffer.getvalue()
    buffer.seek(0)
    
    return buffer
