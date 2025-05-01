from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

def create_styled_resume(data):
    """
    Create a professionally styled resume PDF using ReportLab
    
    Args:
        data (dict): Dictionary containing resume information
        
    Returns:
        BytesIO: PDF file as a BytesIO object
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Flowable elements for the document
    elements = []
    
    # Define colors
    blue_color = colors.HexColor('#4285f4')  # Google blue
    text_color = colors.HexColor('#333333')  # Dark gray
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        alignment=0,  # 0=left aligned
        textColor=text_color,
        spaceAfter=6
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=blue_color,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=text_color,
        spaceAfter=3
    )
    
    info_style = ParagraphStyle(
        'InfoText',
        parent=normal_style,
        fontSize=9,
        spaceAfter=2
    )
    
    # Add name at the top
    elements.append(Paragraph(data['name'], name_style))
    
    # Create a dict for about info icons with text
    about_info = [
        {'text': data['dob']},
        {'text': data['phnum']},
        {'text': f"{data['city']}, {data['state']}"},
        {'text': data['email']}
    ]
    
    # ABOUT ME section
    elements.append(Paragraph("ABOUT ME", section_title_style))
    for info in about_info:
        elements.append(Paragraph(f"• {info['text']}", info_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Career Objectives
    if data['ucareerob']:
        elements.append(Paragraph("CAREER OBJECTIVES", section_title_style))
        elements.append(Paragraph(data['ucareerob'], normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Education
    elements.append(Paragraph("EDUCATION", section_title_style))
    
    # Create education items
    for edu in data['education']:
        if 'course' in edu and 'college' in edu and 'graduation' in edu:
            # Create a table for each education item with course/college on left, graduation date on right
            edu_data = [
                [Paragraph(f"<b>{edu['course']}</b>", normal_style), 
                 Paragraph(f"Graduated, {edu['graduation']}", normal_style)],
                [Paragraph(edu['college'], normal_style), ""]
            ]
            
            t = Table(edu_data, colWidths=[4*inch, 2.5*inch])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 0.1*inch))
    
    # Achievements
    if data['achievements']:
        elements.append(Paragraph("ACHIEVEMENTS", section_title_style))
        for achievement in data['achievements']:
            elements.append(Paragraph(f"• {achievement}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Skills
    if data['skills']:
        elements.append(Paragraph("PERSONAL SKILLS", section_title_style))
        for skill in data['skills']:
            elements.append(Paragraph(f"• {skill}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Personal Details
    elements.append(Paragraph("PERSONAL DETAILS", section_title_style))
    
    # Create a table for personal details
    personal_data = [
        [Paragraph("<b>Father's Name</b>", normal_style), Paragraph(data['fname'], normal_style)],
        [Paragraph("<b>Mother's Name</b>", normal_style), Paragraph(data['mname'], normal_style)],
        [Paragraph("<b>Permanent Address</b>", normal_style), Paragraph(data['paddress'], normal_style)]
    ]
    
    t = Table(personal_data, colWidths=[1.5*inch, 5*inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.2*inch))
    
    # Declaration
    declaration_style = ParagraphStyle(
        'Declaration',
        parent=normal_style,
        fontSize=10,
        spaceBefore=6
    )
    
    elements.append(Paragraph("<b>Declaration</b>", declaration_style))
    declaration_text = f"I, {data['name']}, hereby declare that all the information provided above are correct and complete to the best of my knowledge and belief. I understand that if any time it is found that any information given is false, my appointment is liable to be cancelled."
    elements.append(Paragraph(declaration_text, declaration_style))
    
    # Signature line
    elements.append(Spacer(1, 0.3*inch))
    
    sig_data = [
        [Paragraph("_____________", normal_style), Paragraph(f"{data['city']}, {data['state']}", normal_style)],
        [Paragraph(data['name'], normal_style), ""]
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    elements.append(sig_table)
    
    # Page number
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(
            7.5 * inch,
            0.25 * inch,
            f"1/1"
        )
        canvas.restoreState()
    
    # Build the PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    # Reset the buffer position
    buffer.seek(0)
    
    return buffer
