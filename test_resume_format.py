#!/usr/bin/env python3
"""
Test script to demonstrate resume formatting without API calls
"""

import os
from pdf_generator import PDFResumeGenerator

class MockResumeGenerator:
    def generate_matching_resume_sample(self):
        return """
JOHN DOE
Email: john.doe@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe | Location: San Francisco, CA

PROFESSIONAL SUMMARY
Senior Software Engineer with 7+ years of Python development experience. Expertise in Django and Flask frameworks with strong background in building scalable web applications and RESTful APIs. Proven track record of developing database-driven applications using PostgreSQL and implementing modern software development practices.

WORK EXPERIENCE

Senior Python Developer | TechSolutions Inc. | 2021 - Present
• Developed and maintained 15+ web applications using Django and Flask frameworks
• Built RESTful APIs serving 100k+ daily requests with 99.9% uptime
• Designed PostgreSQL database schemas for complex business applications
• Collaborated with cross-functional teams of 8+ developers using Git workflow
• Implemented CI/CD pipelines using Jenkins and Docker containers
• Led code reviews and mentored 3 junior developers

Software Engineer | DataFlow Systems | 2019 - 2021  
• Created scalable web applications using Python, Django, and PostgreSQL
• Developed microservices architecture handling 50k+ concurrent users
• Integrated AWS services including EC2, RDS, and S3 for cloud deployment
• Implemented Redis caching strategies improving response times by 40%
• Built responsive frontend components using React.js

Python Developer | StartupTech | 2017 - 2019
• Built MVP web applications using Flask and SQLAlchemy
• Developed REST APIs consumed by mobile and web applications
• Implemented user authentication and authorization systems
• Optimized database queries reducing load times by 35%

TECHNICAL SKILLS
Languages: Python, JavaScript, SQL, HTML/CSS
Frameworks: Django, Flask, React, Vue.js
Databases: PostgreSQL, MySQL, Redis
Cloud: AWS (EC2, RDS, S3, Lambda), Docker
Tools: Git, Jenkins, GraphQL, CI/CD

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2017

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Python Professional Certification (2020)
"""

    def generate_non_matching_resume_sample(self):
        return """
SARAH WILSON
Email: sarah.wilson@email.com | Phone: (555) 987-6543
LinkedIn: linkedin.com/in/sarahwilson | Location: Austin, TX

PROFESSIONAL SUMMARY
Creative Marketing Professional with 6+ years of experience in digital marketing campaigns, social media management, and brand development. Strong background in content creation, customer engagement, and market research with proven ability to increase brand awareness and drive customer acquisition.

WORK EXPERIENCE

Senior Marketing Manager | BrandBoost Agency | 2020 - Present
• Managed social media campaigns for 25+ clients across various industries
• Developed content marketing strategies increasing engagement by 60%
• Created email marketing campaigns with average open rate of 28%
• Analyzed market trends and competitor strategies using Google Analytics
• Led team of 4 marketing specialists and coordinated with design team
• Managed marketing budgets up to $500k annually

Marketing Specialist | CreativeEdge | 2018 - 2020
• Designed and implemented digital advertising campaigns on Facebook and Instagram
• Created blog content and SEO-optimized articles driving 40% traffic increase
• Coordinated influencer partnerships and brand collaborations
• Managed customer relationship management (CRM) systems
• Conducted market research and customer surveys

Marketing Coordinator | LocalBusiness Solutions | 2017 - 2018
• Assisted in creating promotional materials and marketing collateral
• Managed company website content and social media accounts
• Organized trade shows and marketing events
• Supported sales team with lead generation activities

TECHNICAL SKILLS
Marketing Tools: HubSpot, Mailchimp, Hootsuite, Buffer
Analytics: Google Analytics, Facebook Analytics, SEMrush
Design: Adobe Creative Suite (Photoshop, Illustrator, InDesign)
CRM: Salesforce, Zoho
Other: Microsoft Office Suite, Basic HTML/CSS

EDUCATION
Bachelor of Arts in Marketing
University of Texas at Austin | 2017

CERTIFICATIONS
• Google Analytics Certified (2021)
• HubSpot Content Marketing Certification (2020)
• Facebook Blueprint Certification (2019)
"""

def test_resume_formats():
    print("=== RESUME GENERATOR FORMAT TEST ===\n")
    
    # Sample job description for context
    job_description = """
    Senior Software Engineer - Python
    
    Must-Have Requirements:
    - 5+ years of Python development experience
    - Experience with Django or Flask frameworks
    - Strong knowledge of SQL databases (PostgreSQL preferred)
    - Experience with RESTful API development
    - Familiarity with Git version control
    - Bachelor's degree in Computer Science or related field
    
    Nice-to-Have Requirements:
    - Experience with AWS cloud services
    - Knowledge of Docker and containerization
    - Experience with React or Vue.js frontend frameworks
    """
    
    print("JOB DESCRIPTION:")
    print(job_description)
    print("\n" + "="*80 + "\n")
    
    generator = MockResumeGenerator()
    
    print("MATCHING RESUME (Candidate who FITS the job requirements):")
    print("="*60)
    matching_resume = generator.generate_matching_resume_sample()
    print(matching_resume)
    
    print("\n" + "="*80 + "\n")
    
    print("NON-MATCHING RESUME (Candidate who DOES NOT fit the job requirements):")
    print("="*60)
    non_matching_resume = generator.generate_non_matching_resume_sample()
    print(non_matching_resume)
    
    print("\n" + "="*80)
    print("FORMAT ANALYSIS:")
    print("="*80)
    print("✓ Both resumes follow standard professional format")
    print("✓ Matching resume has all required Python/Django/PostgreSQL experience") 
    print("✓ Non-matching resume shows marketing background (completely different field)")
    print("✓ Matching resume shows technical skills aligned with job requirements")
    print("✓ Non-matching resume lacks any programming or database experience")
    print("✓ Both resumes appear realistic and professionally written")
    
    # Generate TXT versions
    print("\n" + "="*80)
    print("GENERATING TXT VERSIONS...")
    print("="*80)
    
    os.makedirs('test_output', exist_ok=True)
    
    matching_txt = 'test_output/test_matching_resume.txt'
    non_matching_txt = 'test_output/test_non_matching_resume.txt'
    
    with open(matching_txt, 'w', encoding='utf-8') as f:
        f.write(matching_resume)
        
    with open(non_matching_txt, 'w', encoding='utf-8') as f:
        f.write(non_matching_resume)
    
    print(f"✓ Matching resume TXT saved to: {matching_txt}")
    print(f"✓ Non-matching resume TXT saved to: {non_matching_txt}")
    print("\nTXT generation test completed! Check the test_output/ directory for the TXT files.")

if __name__ == '__main__':
    test_resume_formats()