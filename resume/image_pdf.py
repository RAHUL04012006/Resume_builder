from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import os

def create_image_resume(data):
    """
    Create a professionally styled resume PDF using ReportLab with images from the static folder
    
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
    
    # Path to images
    img_path = os.path.join('static', 'img', 'resume_1')
    
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
    about_icon = Image(os.path.join(img_path, 'about_us_icon.png'))
    about_icon.drawHeight = 0.3*inch
    about_icon.drawWidth = 0.3*inch
    about_table = Table([[about_icon, Paragraph('<b>ABOUT ME</b>', section_title_style)]], 
                        colWidths=[0.4*inch, 6.1*inch])
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
    dob_icon = Image(os.path.join(img_path, 'birthday.png'))
    dob_icon.drawHeight = 0.25*inch
    dob_icon.drawWidth = 0.25*inch
    dob_table = Table([[dob_icon, Paragraph(data['dob'], info_style)]], 
                     colWidths=[0.4*inch, 6.1*inch])
    dob_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(dob_table)
    elements.append(Spacer(1, 0.05*inch))
    
    phone_icon = Image(os.path.join(img_path, 'phone.png'))
    phone_icon.drawHeight = 0.25*inch
    phone_icon.drawWidth = 0.25*inch
    phone_table = Table([[phone_icon, Paragraph(data['phnum'], info_style)]], 
                       colWidths=[0.4*inch, 6.1*inch])
    phone_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(phone_table)
    elements.append(Spacer(1, 0.05*inch))
    
    location_icon = Image(os.path.join(img_path, 'location.png'))
    location_icon.drawHeight = 0.25*inch
    location_icon.drawWidth = 0.25*inch
    location_table = Table([[location_icon, Paragraph(f"{data['city']}, {data['state']}", info_style)]], 
                          colWidths=[0.4*inch, 6.1*inch])
    location_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(location_table)
    elements.append(Spacer(1, 0.05*inch))
    
    email_icon = Image(os.path.join(img_path, 'email.png'))
    email_icon.drawHeight = 0.25*inch
    email_icon.drawWidth = 0.25*inch
    email_table = Table([[email_icon, Paragraph(data['email'], info_style)]], 
                       colWidths=[0.4*inch, 6.1*inch])
    email_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(email_table)
    
    # Career Objectives
    if data['ucareerob']:
        elements.append(Spacer(1, 0.1*inch))
        # Using computer icon for career objectives
        career_icon = Image(os.path.join(img_path, 'computer.png'))
        career_icon.drawHeight = 0.3*inch
        career_icon.drawWidth = 0.3*inch
        career_table = Table([[career_icon, Paragraph('<b>CAREER OBJECTIVES</b>', section_title_style)]], 
                            colWidths=[0.4*inch, 6.1*inch])
        career_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(career_table)
        elements.append(Paragraph(data['ucareerob'], normal_style))
    
    # Education
    elements.append(Spacer(1, 0.1*inch))
    edu_icon = Image(os.path.join(img_path, 'education.png'))
    edu_icon.drawHeight = 0.3*inch
    edu_icon.drawWidth = 0.3*inch
    edu_table = Table([[edu_icon, Paragraph('<b>EDUCATION</b>', section_title_style)]], 
                      colWidths=[0.4*inch, 6.1*inch])
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
        ach_icon = Image(os.path.join(img_path, 'achiements.png'))
        ach_icon.drawHeight = 0.3*inch
        ach_icon.drawWidth = 0.3*inch
        ach_table = Table([[ach_icon, Paragraph('<b>ACHIEVEMENTS</b>', section_title_style)]], 
                          colWidths=[0.4*inch, 6.1*inch])
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
    
    # Skills - using computer icon as a substitute since we don't have a specific skills icon
    if data['skills']:
        elements.append(Spacer(1, 0.1*inch))
        skills_icon = Image(os.path.join(img_path, 'computer.png'))
        skills_icon.drawHeight = 0.3*inch
        skills_icon.drawWidth = 0.3*inch
        skills_table = Table([[skills_icon, Paragraph('<b>PERSONAL SKILLS</b>', section_title_style)]], 
                            colWidths=[0.4*inch, 6.1*inch])
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
    details_icon = Image(os.path.join(img_path, 'personal_info.png'))
    details_icon.drawHeight = 0.3*inch
    details_icon.drawWidth = 0.3*inch
    details_table = Table([[details_icon, Paragraph('<b>PERSONAL DETAILS</b>', section_title_style)]], 
                          colWidths=[0.4*inch, 6.1*inch])
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
