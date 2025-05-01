from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import os

def create_two_column_resume(data):
    """
    Create a two-column professionally styled resume PDF
    
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
    blue_color = colors.HexColor('#8292ee')  # Blue color used in template
    light_blue = colors.HexColor('#e6e9fa')  # Light blue for backgrounds
    text_color = colors.HexColor('#333333')  # Dark gray
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        alignment=0,  # Left aligned
        textColor=text_color,
        spaceAfter=6
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
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
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceAfter=2,
        leading=16
    )
    
    about_style = ParagraphStyle(
        'AboutText',
        parent=normal_style,
        fontSize=10,
        alignment=4,  # Justified
        textColor=text_color
    )
    
    # Add name at the top
    elements.append(Paragraph(data['name'], name_style))
    
    # Add about text if available
    if data.get('uaboutself'):
        elements.append(Paragraph(data['uaboutself'], about_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Create the two-column layout
    left_col_width = 2.5*inch
    right_col_width = 4*inch
    
    # LEFT COLUMN CONTENT
    left_column = []
    
    # About Me section
    about_icon = Image(os.path.join(img_path, 'about_us_icon.png'))
    about_icon.drawHeight = 0.3*inch
    about_icon.drawWidth = 0.3*inch
    
    about_title = Table([[about_icon, Paragraph('<b>ABOUT ME</b>', section_title_style)]], 
                        colWidths=[0.4*inch, 2.1*inch])
    about_title.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    left_column.append(about_title)
    
    # About divider
    about_divider = Table([['']], colWidths=[left_col_width], rowHeights=[1])
    about_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
    left_column.append(about_divider)
    left_column.append(Spacer(1, 0.1*inch))
    
    # Personal info with icons
    icons = [
        ('birthday.png', data['dob']),
        ('phone.png', data['phnum']),
        ('location.png', f"{data['city']}, {data['state']}"),
        ('email.png', data['email'])
    ]
    
    for icon_name, text in icons:
        icon = Image(os.path.join(img_path, icon_name))
        icon.drawHeight = 0.25*inch
        icon.drawWidth = 0.25*inch
        row = Table([[icon, Paragraph(text, info_style)]], 
                   colWidths=[0.4*inch, 2.1*inch])
        row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        left_column.append(row)
        left_column.append(Spacer(1, 0.05*inch))
    
    # Skills section
    left_column.append(Spacer(1, 0.2*inch))
    skills_icon = Image(os.path.join(img_path, 'computer.png'))
    skills_icon.drawHeight = 0.3*inch
    skills_icon.drawWidth = 0.3*inch
    
    skills_title = Table([[skills_icon, Paragraph('<b>PERSONAL SKILLS</b>', section_title_style)]], 
                         colWidths=[0.4*inch, 2.1*inch])
    skills_title.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    left_column.append(skills_title)
    
    skills_divider = Table([['']], colWidths=[left_col_width], rowHeights=[1])
    skills_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
    left_column.append(skills_divider)
    left_column.append(Spacer(1, 0.1*inch))
    
    if data.get('skills'):
        for skill in data['skills']:
            left_column.append(Paragraph(f"• {skill}", normal_style))
    
    # Personal Details section
    left_column.append(Spacer(1, 0.2*inch))
    personal_icon = Image(os.path.join(img_path, 'personal_info.png'))
    personal_icon.drawHeight = 0.3*inch
    personal_icon.drawWidth = 0.3*inch
    
    personal_title = Table([[personal_icon, Paragraph('<b>PERSONAL DETAILS</b>', section_title_style)]], 
                          colWidths=[0.4*inch, 2.1*inch])
    personal_title.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    left_column.append(personal_title)
    
    personal_divider = Table([['']], colWidths=[left_col_width], rowHeights=[1])
    personal_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
    left_column.append(personal_divider)
    left_column.append(Spacer(1, 0.1*inch))
    
    personal_details = [
        f"<b>Father's Name:</b> {data.get('fname', '')}",
        f"<b>Mother's Name:</b> {data.get('mname', '')}",
        f"<b>Permanent Address:</b> {data.get('paddress', '')}"
    ]
    
    for detail in personal_details:
        left_column.append(Paragraph(detail, normal_style))
    
    # RIGHT COLUMN CONTENT
    right_column = []
    
    # Career Objectives
    if data.get('ucareerob'):
        right_column.append(Paragraph('<b>CAREER OBJECTIVES</b>', section_title_style))
        career_divider = Table([['']], colWidths=[right_col_width], rowHeights=[1])
        career_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
        right_column.append(career_divider)
        right_column.append(Spacer(1, 0.1*inch))
        right_column.append(Paragraph(data['ucareerob'], normal_style))
        right_column.append(Spacer(1, 0.2*inch))
    
    # Education
    if data.get('education'):
        edu_icon = Image(os.path.join(img_path, 'education.png'))
        edu_icon.drawHeight = 0.3*inch
        edu_icon.drawWidth = 0.3*inch
        
        edu_title = Table([[edu_icon, Paragraph('<b>EDUCATION</b>', section_title_style)]], 
                          colWidths=[0.4*inch, 3.6*inch])
        edu_title.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        right_column.append(edu_title)
        
        edu_divider = Table([['']], colWidths=[right_col_width], rowHeights=[1])
        edu_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
        right_column.append(edu_divider)
        right_column.append(Spacer(1, 0.1*inch))
        
        for edu in data['education']:
            if 'course' in edu and 'college' in edu and 'graduation' in edu:
                edu_data = [
                    [Paragraph(f"<b>{edu['course']}</b>", normal_style), 
                     Paragraph(f"Graduated, {edu['graduation']}", normal_style)],
                    [Paragraph(edu['college'], normal_style), ""]
                ]
                t = Table(edu_data, colWidths=[3*inch, 1*inch])
                t.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ]))
                right_column.append(t)
                right_column.append(Spacer(1, 0.1*inch))
    
    # Achievements
    if data.get('achievements'):
        right_column.append(Spacer(1, 0.2*inch))
        ach_icon = Image(os.path.join(img_path, 'achiements.png'))
        ach_icon.drawHeight = 0.3*inch
        ach_icon.drawWidth = 0.3*inch
        
        ach_title = Table([[ach_icon, Paragraph('<b>ACHIEVEMENTS</b>', section_title_style)]], 
                          colWidths=[0.4*inch, 3.6*inch])
        ach_title.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        right_column.append(ach_title)
        
        ach_divider = Table([['']], colWidths=[right_col_width], rowHeights=[1])
        ach_divider.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, blue_color)]))
        right_column.append(ach_divider)
        right_column.append(Spacer(1, 0.1*inch))
        
        for achievement in data['achievements']:
            right_column.append(Paragraph(f"• {achievement}", normal_style))
    
    # Combine left and right columns
    main_table = Table([[left_column, right_column]], 
                       colWidths=[left_col_width, right_col_width])
    main_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    
    elements.append(main_table)
    
    # Declaration section
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph('<b>DECLARATION</b>', section_title_style))
    declaration_text = f"I, {data['name']}, hereby declare that all the information provided above are correct and complete to the best of my knowledge and belief. I understand that if any time it is found that any information given is false, my appointment is liable to be cancelled."
    elements.append(Paragraph(declaration_text, normal_style))
    
    # Signature and place
    signature_table = Table([
        [Paragraph("____________________________", normal_style), 
         Paragraph(f"Place: {data.get('city', '')}", normal_style)],
        [Paragraph(data['name'], normal_style), ""]
    ], colWidths=[3*inch, 3.5*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    elements.append(signature_table)
    
    # Build the PDF
    doc.build(elements)
    
    # Reset buffer position
    buffer.seek(0)
    return buffer
