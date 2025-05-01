from flask import render_template, make_response
import pdfkit
from io import BytesIO

def create_pdf_from_html(template_name, data):
    """
    Create a PDF from HTML template using pdfkit
    
    Args:
        template_name (str): Name of the HTML template
        data (dict): Data to be used in the template
        
    Returns:
        BytesIO: PDF data as BytesIO object
    """
    # Render the HTML template with the provided data
    html = render_template(template_name, data=data)
    
    # Configure pdfkit options
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8',
        'quiet': '',
        'no-outline': None
    }
    
    # Create PDF from HTML
    pdf = pdfkit.from_string(html, False, options=options)
    
    # Return the PDF data
    return pdf
