from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

def create_enhanced_resume(data):
    """
    Create a professional PDF resume with enhanced styling
    
    Args:
        data: Dictionary containing resume information
        
    Returns:
        BytesIO buffer containing the PDF data
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document with smaller margins
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define professional colors
    primary_color = colors.HexColor("#2c3e50")  # Dark blue
    accent_color = colors.HexColor("#3498db")   # Light blue
    
    # Create professional styles
    title_style = ParagraphStyle(
        name='ResumeTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        alignment=1,  # Center
        spaceAfter=12,
        textColor=primary_color
    )
    
    subtitle_style = ParagraphStyle(
        name='ResumeSubtitle',
        fontName='Helvetica',
        fontSize=12,
        alignment=1,
        spaceAfter=24,
        textColor=accent_color
    )
    
    section_style = ParagraphStyle(
        name='ResumeSection',
        fontName='Helvetica-Bold',
        fontSize=14,
        alignment=0,
        spaceAfter=8,
        spaceBefore=12,
        textColor=accent_color
    )
    
    normal_style = ParagraphStyle(
        name='ResumeNormal',
        fontName='Helvetica',
        fontSize=11,
        alignment=0,
        spaceAfter=6,
        textColor=primary_color,
        leading=14  # Line spacing
    )
    
    # Create header with name and contact info
    elements.append(Paragraph(data['name'], title_style))
    
    # Contact information
    contact_info = f"Email: {data['email']} | Phone: {data['phnum']} | {data['city']}, {data['state']}"
    elements.append(Paragraph(contact_info, subtitle_style))
    
    # Add a horizontal line
    t = Table([['']],
       colWidths=[7.5*inch],
       rowHeights=[2],
       style=TableStyle([
           ('LINEABOVE', (0, 0), (-1, 0), 1, accent_color),
       ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Career Objective
    if data['ucareerob']:
        elements.append(Paragraph('<u>Career Objective</u>', section_style))
        elements.append(Paragraph(data['ucareerob'], normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # About
    if data['uaboutself']:
        elements.append(Paragraph('<u>About</u>', section_style))
        elements.append(Paragraph(data['uaboutself'], normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Light divider
    t = Table([['']],
       colWidths=[7.5*inch],
       rowHeights=[1],
       style=TableStyle([
           ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
       ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Education
    if data['education']:
        elements.append(Paragraph('<u>Education</u>', section_style))
        for edu in data['education']:
            if 'course' in edu and 'college' in edu and 'graduation' in edu:
                course_style = ParagraphStyle(
                    name='ResumeCourse',
                    parent=normal_style,
                    textColor=accent_color,
                    fontName='Helvetica-Bold'
                )
                elements.append(Paragraph(f"<b>{edu['course']}</b>", course_style))
                elements.append(Paragraph(f"{edu['college']}, <i>{edu['graduation']}</i>", normal_style))
                elements.append(Spacer(1, 0.05*inch))
        elements.append(Spacer(1, 0.1*inch))
    
    # Light divider
    t = Table([['']],
       colWidths=[7.5*inch],
       rowHeights=[1],
       style=TableStyle([
           ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
       ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Skills
    if data['skills']:
        elements.append(Paragraph('<u>Skills</u>', section_style))
        
        # Set up data for a table with skills
        skill_data = []
        row = []
        col_count = 0
        
        for skill in data['skills']:
            col_count += 1
            row.append(Paragraph(f"• {skill}", normal_style))
            
            if col_count == 3:  # 3 skills per row
                skill_data.append(row)
                row = []
                col_count = 0
        
        # Add any remaining skills
        if row:
            while len(row) < 3:
                row.append("")
            skill_data.append(row)
        
        # Create table for skills
        if skill_data:
            skill_table = Table(skill_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
            skill_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(skill_table)
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Light divider
    t = Table([['']],
       colWidths=[7.5*inch],
       rowHeights=[1],
       style=TableStyle([
           ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
       ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Achievements
    if data['achievements']:
        elements.append(Paragraph('<u>Achievements</u>', section_style))
        for achievement in data['achievements']:
            elements.append(Paragraph(f"• {achievement}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Light divider
    t = Table([['']],
       colWidths=[7.5*inch],
       rowHeights=[1],
       style=TableStyle([
           ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
       ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))
    
    # Personal Details in a nicer format
    elements.append(Paragraph('<u>Personal Details</u>', section_style))
    
    # Create a 2-column table for personal details
    personal_data = [
        [Paragraph("<b>Father's Name:</b>", normal_style), Paragraph(data['fname'], normal_style)],
        [Paragraph("<b>Mother's Name:</b>", normal_style), Paragraph(data['mname'], normal_style)],
        [Paragraph("<b>Date of Birth:</b>", normal_style), Paragraph(data['dob'], normal_style)],
        [Paragraph("<b>Permanent Address:</b>", normal_style), Paragraph(data['paddress'], normal_style)]
    ]
    
    personal_table = Table(personal_data, colWidths=[1.5*inch, 6.0*inch])
    personal_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(personal_table)
    
    # Footer with page numbers
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num = f"Page {doc.page}"
        canvas.drawRightString(
            7.5 * inch,
            0.25 * inch,
            page_num
        )
        # Add a footer line
        canvas.setStrokeColor(colors.grey)
        canvas.line(0.5*inch, 0.5*inch, 8*inch, 0.5*inch)
        canvas.restoreState()
    
    # Build the PDF with page numbers
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    # Reset the buffer position
    buffer.seek(0)
    
    return buffer
