from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import black, darkblue, grey
import re

class PDFResumeGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        # Name styling
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Normal'],
            fontSize=22,
            spaceAfter=4,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=darkblue,
            leading=26
        ))
        
        # Contact info styling
        self.styles.add(ParagraphStyle(
            name='Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=16,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica',
            textColor=black,
            leading=12
        ))
        
        # Section headers with line
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            textColor=darkblue,
            borderWidth=0,
            borderPadding=0,
            leading=16
        ))
        
        # Professional summary
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            spaceBefore=0,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=2,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            textColor=black,
            leading=14
        ))
        
        # Company and dates
        self.styles.add(ParagraphStyle(
            name='CompanyDates',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=0,
            fontName='Helvetica-Oblique',
            textColor=grey,
            leading=12
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            spaceBefore=0,
            fontName='Helvetica',
            leftIndent=0,
            bulletIndent=0,
            leading=13
        ))
        
        # Skills section
        self.styles.add(ParagraphStyle(
            name='Skills',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=0,
            fontName='Helvetica',
            leading=13
        ))
        
        # Education
        self.styles.add(ParagraphStyle(
            name='Education',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=0,
            fontName='Helvetica',
            leading=13
        ))
    
    def _parse_resume_text(self, resume_text):
        lines = [line.strip() for line in resume_text.strip().split('\n') if line.strip()]
        
        parsed = {
            'name': '',
            'contact': '',
            'summary': '',
            'experience': [],
            'skills': '',
            'education': '',
            'certifications': ''
        }
        
        current_section = None
        current_job = None
        
        for line in lines:
            # Skip separator lines
            if line.startswith('══════'):
                continue
                
            line_upper = line.upper()
            
            # Extract name (remove emojis if present)
            if not parsed['name'] and not line.startswith(('📧', 'Email:', 'Phone:', 'LinkedIn:', '💼', '🛠️', '🎓', '🏅')):
                # Clean name of any leading emojis
                clean_name = re.sub(r'^[^\w\s]+\s*', '', line)
                if clean_name.strip() and not any(keyword in clean_name.upper() for keyword in ['SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION']):
                    parsed['name'] = clean_name.strip()
                continue
            
            # Handle emoji-formatted contact info
            if line.startswith('📧') or line.startswith('Email:') or ('📞' in line and '🌍' in line and '💼' in line):
                # Extract contact info and clean emojis for PDF
                contact_line = re.sub(r'[📧📞🌍💼]\s*', '', line)
                parsed['contact'] = contact_line
                continue
            
            # Section detection with emoji support
            if ('💼' in line and 'PROFESSIONAL SUMMARY' in line_upper) or 'PROFESSIONAL SUMMARY' in line_upper:
                current_section = 'summary'
                continue
            elif ('💼' in line and 'PROFESSIONAL EXPERIENCE' in line_upper) or 'WORK EXPERIENCE' in line_upper or 'PROFESSIONAL EXPERIENCE' in line_upper:
                current_section = 'experience'
                continue
            elif ('🛠️' in line and 'TECHNICAL EXPERTISE' in line_upper) or 'TECHNICAL SKILLS' in line_upper or 'TECHNICAL EXPERTISE' in line_upper:
                current_section = 'skills'
                continue
            elif ('🎓' in line and 'EDUCATION' in line_upper) or 'EDUCATION' in line_upper:
                current_section = 'education'
                continue
            elif ('🏅' in line and 'CERTIFICATIONS' in line_upper) or 'CERTIFICATIONS' in line_upper:
                current_section = 'certifications'
                continue
            
            if current_section == 'summary':
                # Clean emojis from summary content
                clean_line = re.sub(r'[💼🛠️🎓🏅🚀📧📞🌍🏢📅📍]\s*', '', line)
                if clean_line.strip():
                    parsed['summary'] += clean_line + ' '
            elif current_section == 'experience':
                # Handle emoji-formatted experience entries
                if line.startswith('🏢'):
                    # Company-title line
                    if current_job:
                        parsed['experience'].append(current_job)
                    clean_line = re.sub(r'[🏢]\s*', '', line)
                    if ' - ' in clean_line:
                        parts = clean_line.split(' - ', 1)
                        current_job = {
                            'title': parts[1].strip() if len(parts) > 1 else clean_line.strip(),
                            'company': parts[0].strip() if len(parts) > 1 else '',
                            'dates': '',
                            'bullets': []
                        }
                    else:
                        current_job = {
                            'title': clean_line.strip(),
                            'company': '',
                            'dates': '',
                            'bullets': []
                        }
                elif line.startswith('📅') and current_job:
                    # Date-location line
                    clean_line = re.sub(r'[📅📍]\s*', '', line)
                    if '|' in clean_line:
                        parts = clean_line.split('|')
                        current_job['dates'] = parts[0].strip()
                        current_job['company'] += f" | {parts[1].strip()}" if len(parts) > 1 else ""
                    else:
                        current_job['dates'] = clean_line.strip()
                elif line.startswith('•') and current_job:
                    current_job['bullets'].append(line[1:].strip())
                elif '|' in line and not line.startswith('•') and not line.startswith('🏢') and not line.startswith('📅'):
                    # Fallback for traditional format
                    if current_job:
                        parsed['experience'].append(current_job)
                    parts = line.split('|')
                    current_job = {
                        'title': parts[0].strip(),
                        'company': parts[1].strip() if len(parts) > 1 else '',
                        'dates': parts[2].strip() if len(parts) > 2 else '',
                        'bullets': []
                    }
            elif current_section == 'skills':
                # Clean emojis from skills
                clean_line = re.sub(r'[🛠️💼🎓🏅]\s*', '', line)
                if clean_line.strip():
                    parsed['skills'] += clean_line + '\n'
            elif current_section == 'education':
                # Clean emojis from education
                clean_line = re.sub(r'[🎓📚🏅]\s*', '', line)
                if clean_line.strip():
                    parsed['education'] += clean_line + '\n'
            elif current_section == 'certifications':
                # Clean emojis from certifications
                clean_line = re.sub(r'[🏅🎓]\s*', '', line)
                if clean_line.strip():
                    parsed['certifications'] += clean_line + '\n'
        
        if current_job:
            parsed['experience'].append(current_job)
        
        parsed['contact'] = parsed['contact'].rstrip(' | ')
        return parsed
    
    def create_pdf_resume(self, resume_text, filename):
        # Reduced top margin to remove extra spacing
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.5*inch, bottomMargin=0.75*inch)
        
        story = []
        parsed = self._parse_resume_text(resume_text)
        
        # Name with no top spacing
        if parsed['name']:
            story.append(Paragraph(parsed['name'], self.styles['Name']))
        
        # Contact info
        if parsed['contact']:
            story.append(Paragraph(parsed['contact'], self.styles['Contact']))
        
        # Professional Summary with section line
        if parsed['summary']:
            story.append(self._create_section_header("PROFESSIONAL SUMMARY"))
            story.append(Paragraph(parsed['summary'].strip(), self.styles['Summary']))
        
        # Work Experience
        if parsed['experience']:
            story.append(self._create_section_header("WORK EXPERIENCE"))
            for i, job in enumerate(parsed['experience']):
                if job['title']:
                    story.append(Paragraph(job['title'], self.styles['JobTitle']))
                
                if job['company'] or job['dates']:
                    company_info = f"{job['company']} | {job['dates']}" if job['company'] and job['dates'] else job['company'] or job['dates']
                    story.append(Paragraph(company_info, self.styles['CompanyDates']))
                
                # Bullet points with proper spacing
                for bullet in job['bullets']:
                    story.append(Paragraph(f"• {bullet}", self.styles['BulletPoint']))
                
                # Add spacing between jobs (except after last job)
                if i < len(parsed['experience']) - 1:
                    story.append(Spacer(1, 6))
        
        # Technical Skills
        if parsed['skills']:
            story.append(self._create_section_header("TECHNICAL SKILLS"))
            for line in parsed['skills'].strip().split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), self.styles['Skills']))
        
        # Education
        if parsed['education']:
            story.append(self._create_section_header("EDUCATION"))
            for line in parsed['education'].strip().split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), self.styles['Education']))
        
        # Certifications
        if parsed['certifications']:
            story.append(self._create_section_header("CERTIFICATIONS"))
            for line in parsed['certifications'].strip().split('\n'):
                if line.strip():
                    story.append(Paragraph(line.strip(), self.styles['Education']))
        
        doc.build(story)
        return filename
    
    def _create_section_header(self, title):
        """Create a section header with a horizontal line underneath"""
        from reportlab.platypus import KeepTogether
        
        header_elements = []
        header_elements.append(Paragraph(title, self.styles['SectionHeader']))
        header_elements.append(HRFlowable(width="100%", thickness=1, color=darkblue, 
                                        spaceAfter=6, spaceBefore=2))
        
        return KeepTogether(header_elements)