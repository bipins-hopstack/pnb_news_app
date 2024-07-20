#Report lab
import streamlit as st
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import unicodedata
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

def clean_text(text):
    # Remove any non-printable characters
    return ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')

def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(7.5*inch, 0.5*inch, text)

def add_page_border_and_header_footer(canvas, doc):
    canvas.saveState()
    
    # Draw border
    canvas.setStrokeColor(colors.HexColor("#A20E37"))
    canvas.setLineWidth(2)
    canvas.rect(doc.leftMargin, doc.bottomMargin,
                doc.width, doc.height, stroke=1, fill=0)
    
    # Add header
    #canvas.setFont("Helvetica-Bold", 12)
    #canvas.drawString(doc.leftMargin + 0.25*inch, doc.height + doc.topMargin - 0.25*inch, "Document Header")
    
    # Add page number
    page_num = canvas.getPageNumber()
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(7.5*inch, 0.75*inch, f"Page {page_num}")
    
    # Add disclaimer as footer
    disclaimer_text = "Disclaimer: This daily bulletin is not a publication of the Bank. The opinion/views expressed in this bulletin is of various independent newspapers/publications and does not reflect that of the Bank's or its subsidiaries. Bank is not liable in any manner for the facts/ figures represented in the bulletin. Any reliance on such financials by anyone shall be at their own risk/responsibility."
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        fontSize=6,
        leading=8,
        alignment=TA_LEFT
    )
    disclaimer_paragraph = Paragraph(disclaimer_text, disclaimer_style)
    disclaimer_paragraph.wrapOn(canvas, doc.width, doc.bottomMargin)
    disclaimer_paragraph.drawOn(canvas, doc.leftMargin, 0.25*inch)
    
    canvas.restoreState()


def create_category_content(df, category_name):
    content = []
    styles = getSampleStyleSheet()
    
    # Category Title with background color
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        textColor=colors.white,  # White text for better contrast
        fontSize=16,
        leading=20
    )
    title_para = Paragraph(clean_text(category_name), title_style)
    
    # Create a table for the title with background color
    title_table = Table([[title_para]], colWidths=[7*inch])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#FBBC09")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(title_table)
    content.append(Spacer(1, 10))
    
    # Content
    for _, row in df.iterrows():
        try:
            # Article Heading
            heading_style = ParagraphStyle('Heading2', parent=styles['Heading2'], textColor=colors.HexColor("#A20E37"))
            content.append(Paragraph(clean_text(row['Headings']), heading_style))
            
            # Article Summary
            summary_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=8, leading=10)
            content.append(Paragraph(clean_text(row['Summary']), summary_style))
            content.append(Spacer(1, 5))

            # Article Summary
            link_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=6, leading=10, textColor=colors.HexColor("#A20E37"))
            content.append(Paragraph(clean_text(row['Link']), link_style))
            
        except Exception as e:
            print(f"Error processing row: {e}")
            continue  # Skip this row and continue with the next
    
    return KeepTogether(content)

def generate_full_pdf(df1, df2, df3):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            leftMargin=0.5*inch, rightMargin=0.5*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    try:
        story.append(create_category_content(df1, "RBI News"))
        story.append(PageBreak())
        story.append(create_category_content(df2, "SEBI & IRDAI News"))
        story.append(PageBreak())
        story.append(create_category_content(df3, "PIB News"))
        doc.build(story, onFirstPage=add_page_border_and_header_footer, onLaterPages=add_page_border_and_header_footer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None  # Return None if PDF generation fails
