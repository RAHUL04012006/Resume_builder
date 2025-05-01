from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

def create_pdf_resume(data):
    """
    Create a PDF resume using ReportLab
    
    Args:
        data: Dictionary containing resume information
        
    Returns:
        BytesIO buffer containing the PDF data
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Create custom styles with unique names to avoid conflicts
    title_style = ParagraphStyle(
        name='CustomTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=1,  # 0=left, 1=center, 2=right
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        name='CustomHeading',
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=0,
        spaceAfter=8,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        name='CustomNormal',
        fontName='Helvetica',
        fontSize=12,
        alignment=0,
        spaceAfter=6
    )
    
    # Title
    elements.append(Paragraph(data['name'], title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Contact information
    contact_info = f"Email: {data['email']} | Phone: {data['phnum']} | {data['city']}, {data['state']}"
    elements.append(Paragraph(contact_info, normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Career Objective
    if data['ucareerob']:
        elements.append(Paragraph("Career Objective", heading_style))
        elements.append(Paragraph(data['ucareerob'], normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # About
    if data['uaboutself']:
        elements.append(Paragraph("About", heading_style))
        elements.append(Paragraph(data['uaboutself'], normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Education
    if data['education']:
        elements.append(Paragraph("Education", heading_style))
        for edu in data['education']:
            if 'course' in edu and 'college' in edu and 'graduation' in edu:
                edu_text = f"<b>{edu['course']}</b> - {edu['college']}, {edu['graduation']}"
                elements.append(Paragraph(edu_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Skills
    if data['skills']:
        elements.append(Paragraph("Skills", heading_style))
        for skill in data['skills']:
            elements.append(Paragraph(f"• {skill}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Achievements
    if data['achievements']:
        elements.append(Paragraph("Achievements", heading_style))
        for achievement in data['achievements']:
            elements.append(Paragraph(f"• {achievement}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Personal Details
    elements.append(Paragraph("Personal Details", heading_style))
    elements.append(Paragraph(f"<b>Father's Name:</b> {data['fname']}", normal_style))
    elements.append(Paragraph(f"<b>Mother's Name:</b> {data['mname']}", normal_style))
    elements.append(Paragraph(f"<b>Date of Birth:</b> {data['dob']}", normal_style))
    elements.append(Paragraph(f"<b>Permanent Address:</b> {data['paddress']}", normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Reset the buffer position
    buffer.seek(0)
    
    return buffer
