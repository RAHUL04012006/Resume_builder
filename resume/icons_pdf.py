from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Circle, String
from io import BytesIO

def create_icon(icon_text, size=12, color=colors.white, bg_color=colors.HexColor('#4285f4')):
    """Create a small circular icon with text inside"""
    d = Drawing(16, 16)
    # Draw circle
    d.add(Circle(8, 8, 7, fillColor=bg_color, strokeColor=None))
    # Add text
    d.add(String(8, 6, icon_text, fontSize=size, fillColor=color, textAnchor='middle'))
    return d

def create_professional_resume(data):
    """
    Create a professionally styled resume PDF using ReportLab with icons
    
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
        alignment=1,  # Center aligned
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
        spaceAfter=6,
        leading=16
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
        spaceAfter=2,
        leading=16
    )
    
    # Add name at the top
    elements.append(Paragraph(data['name'], name_style))
    
    # Separator line after name
    elements.append(Spacer(1, 0.05*inch))
    t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # ABOUT ME section with icon
    about_icon = create_icon('i')
    about_table = Table([[about_icon, Paragraph('<b>ABOUT ME</b>', section_title_style)]], 
                        colWidths=[0.25*inch, 6.25*inch])
    about_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(about_table)
    
    # Separator line
    t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # About info with icons
    about_info = [
        {'icon': 'd', 'text': data['dob']},
        {'icon': 'p', 'text': data['phnum']},
        {'icon': 'l', 'text': f"{data['city']}, {data['state']}"},
        {'icon': '@', 'text': data['email']}
    ]
    
    for info in about_info:
        icon = create_icon(info['icon'], size=10)
        info_table = Table([[icon, Paragraph(info['text'], info_style)]], 
                          colWidths=[0.25*inch, 6.25*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(info_table)
    
    # Career Objectives
    if data['ucareerob']:
        elements.append(Spacer(1, 0.1*inch))
        career_icon = create_icon('c')
        career_table = Table([[career_icon, Paragraph('<b>CAREER OBJECTIVES</b>', section_title_style)]], 
                            colWidths=[0.25*inch, 6.25*inch])
        career_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(career_table)
        elements.append(Paragraph(data['ucareerob'], normal_style))
    
    # Education
    elements.append(Spacer(1, 0.1*inch))
    edu_icon = create_icon('e')
    edu_table = Table([[edu_icon, Paragraph('<b>EDUCATION</b>', section_title_style)]], 
                      colWidths=[0.25*inch, 6.25*inch])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(edu_table)
    
    # Separator line
    t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
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
        ach_icon = create_icon('a')
        ach_table = Table([[ach_icon, Paragraph('<b>ACHIEVEMENTS</b>', section_title_style)]], 
                          colWidths=[0.25*inch, 6.25*inch])
        ach_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(ach_table)
        
        # Separator line
        t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.1*inch))
        
        # Add achievements as bullet points
        for achievement in data['achievements']:
            elements.append(Paragraph(f"• {achievement}", normal_style))
    
    # Skills
    if data['skills']:
        elements.append(Spacer(1, 0.1*inch))
        skills_icon = create_icon('s')
        skills_table = Table([[skills_icon, Paragraph('<b>PERSONAL SKILLS</b>', section_title_style)]], 
                            colWidths=[0.25*inch, 6.25*inch])
        skills_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(skills_table)
        
        # Separator line
        t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.1*inch))
        
        # Add skills as bullet points
        for skill in data['skills']:
            elements.append(Paragraph(f"• {skill}", normal_style))
    
    # Personal Details
    elements.append(Spacer(1, 0.1*inch))
    details_icon = create_icon('p')
    details_table = Table([[details_icon, Paragraph('<b>PERSONAL DETAILS</b>', section_title_style)]], 
                          colWidths=[0.25*inch, 6.25*inch])
    details_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(details_table)
    
    # Separator line
    t = Table([['']],  colWidths=[6.5*inch], rowHeights=[1])
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Create a table for personal details
    personal_data = [
        [Paragraph("<b>Father's Name:</b>", normal_style), Paragraph(data['fname'], normal_style)],
        [Paragraph("<b>Mother's Name:</b>", normal_style), Paragraph(data['mname'], normal_style)],
        [Paragraph("<b>Permanent Address:</b>", normal_style), Paragraph(data['paddress'], normal_style)]
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
        [Paragraph("_________________", normal_style), Paragraph(f"{data['city']}, {data['state']}", normal_style)],
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
