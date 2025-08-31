import os
import json
from typing import Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from pdf_generator import PDFResumeGenerator

load_dotenv()

class ResumeGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.pdf_generator = PDFResumeGenerator()
        
        # Industry classification mappings
        self.industry_mappings = {
            'technology': {
                'keywords': ['software', 'tech', 'developer', 'engineer', 'programming', 'coding', 'IT', 'computer'],
                'focus_areas': ['Technical Skills', 'Programming Languages', 'Frameworks & Tools', 'Software Development', 'System Architecture'],
                'metrics': ['performance improvements', 'system scalability', 'user base growth', 'uptime', 'response times'],
                'companies': ['TechCorp', 'InnovateSoft', 'DataFlow Systems', 'CloudTech Solutions', 'DevTools Inc.'],
                'achievements': ['Improved system performance by {}%', 'Led team of {} developers', 'Deployed applications serving {}+ users'],
                'optional_sections': ['Technical Projects', 'Open Source Contributions', 'Technical Publications']
            },
            'marketing': {
                'keywords': ['marketing', 'digital', 'advertising', 'campaign', 'brand', 'social media', 'content'],
                'focus_areas': ['Digital Marketing', 'Campaign Management', 'Analytics & Reporting', 'Social Media', 'Content Strategy'],
                'metrics': ['ROI', 'conversion rates', 'engagement rates', 'lead generation', 'campaign performance'],
                'companies': ['BrandBoost Marketing', 'DigitalEdge Agency', 'MarketPro Solutions', 'Creative Campaigns Inc.', 'GrowthHacker Co.'],
                'achievements': ['Increased ROI by {}%', 'Generated {}+ qualified leads', 'Improved conversion rates by {}%'],
                'optional_sections': ['Notable Campaigns', 'Awards & Recognition', 'Speaking Engagements']
            },
            'data_science': {
                'keywords': ['data', 'analytics', 'scientist', 'machine learning', 'AI', 'statistics', 'modeling'],
                'focus_areas': ['Machine Learning', 'Statistical Analysis', 'Data Visualization', 'Programming', 'Research & Development'],
                'metrics': ['model accuracy', 'data processing speed', 'prediction accuracy', 'cost savings', 'automation'],
                'companies': ['DataInsights Corp', 'Analytics Pro', 'ML Solutions Inc.', 'PredictiveEdge', 'Intelligence Systems'],
                'achievements': ['Improved model accuracy by {}%', 'Processed {}+ GB of data daily', 'Reduced analysis time by {}%'],
                'optional_sections': ['Research Publications', 'Data Science Projects', 'Conference Presentations']
            },
            'finance': {
                'keywords': ['finance', 'financial', 'accounting', 'investment', 'banking', 'analyst', 'risk'],
                'focus_areas': ['Financial Analysis', 'Risk Management', 'Investment Strategy', 'Compliance', 'Financial Reporting'],
                'metrics': ['revenue growth', 'cost reduction', 'portfolio performance', 'risk mitigation', 'compliance rates'],
                'companies': ['FinanceFirst Corp', 'Capital Advisors', 'Risk Management Solutions', 'Investment Partners', 'Financial Analytics'],
                'achievements': ['Managed portfolio worth ${}M', 'Reduced operational costs by {}%', 'Achieved {}% return on investments'],
                'optional_sections': ['Professional Licenses', 'Investment Track Record', 'Risk Management Initiatives']
            },
            'healthcare': {
                'keywords': ['healthcare', 'medical', 'clinical', 'patient', 'hospital', 'nursing', 'therapy'],
                'focus_areas': ['Patient Care', 'Clinical Procedures', 'Healthcare Technology', 'Compliance', 'Quality Improvement'],
                'metrics': ['patient outcomes', 'satisfaction scores', 'treatment efficiency', 'compliance rates', 'cost per patient'],
                'companies': ['HealthCare Partners', 'Medical Excellence Center', 'Patient First Hospital', 'Clinical Solutions Inc.', 'WellCare Systems'],
                'achievements': ['Improved patient satisfaction by {}%', 'Treated {}+ patients annually', 'Reduced treatment time by {}%'],
                'optional_sections': ['Medical Licenses', 'Clinical Research', 'Professional Memberships']
            },
            'sales': {
                'keywords': ['sales', 'business development', 'account management', 'revenue', 'client relations'],
                'focus_areas': ['Sales Strategy', 'Client Relationship Management', 'Revenue Generation', 'Market Analysis', 'Negotiation'],
                'metrics': ['revenue generated', 'quota achievement', 'client retention', 'deal closure rates', 'territory growth'],
                'companies': ['SalesForce Solutions', 'Revenue Growth Partners', 'ClientFirst Sales', 'Business Development Corp', 'Market Leaders Inc.'],
                'achievements': ['Generated ${}M in revenue', 'Exceeded quota by {}%', 'Maintained {}% client retention rate'],
                'optional_sections': ['Sales Awards', 'Key Client Relationships', 'Sales Training & Development']
            }
        }
    
    def classify_industry(self, job_analysis: Dict) -> str:
        """
        Classify the industry type based on job analysis data
        """
        industry_text = (
            str(job_analysis.get('industry', '')) + ' ' +
            str(job_analysis.get('job_title', '')) + ' ' +
            str(job_analysis.get('must_have', [])) + ' ' +
            str(job_analysis.get('nice_to_have', []))
        ).lower()
        
        # Count keyword matches for each industry
        industry_scores = {}
        for industry, data in self.industry_mappings.items():
            score = sum(1 for keyword in data['keywords'] if keyword in industry_text)
            industry_scores[industry] = score
        
        # Return the industry with the highest score, default to 'technology' if no matches
        return max(industry_scores, key=industry_scores.get) if max(industry_scores.values()) > 0 else 'technology'
    
    
    def generate_contact_info(self, is_matching: bool = True) -> str:
        """Generate realistic contact information"""
        names = [
            "Michael Rodriguez", "Sarah Chen", "David Patel", "Lisa Thompson", "James Wilson",
            "Emily Garcia", "Alex Johnson", "Maria Gonzalez", "Kevin Lee", "Ashley Brown",
            "Ryan Kim", "Jessica Martinez", "Daniel Singh", "Amanda Davis", "Christopher Wang"
        ]
        
        cities = [
            "Seattle, WA", "Austin, TX", "Denver, CO", "Boston, MA", "Portland, OR",
            "San Francisco, CA", "Chicago, IL", "Atlanta, GA", "Raleigh, NC", "Miami, FL"
        ]
        
        import random
        name = random.choice(names)
        city = random.choice(cities)
        first_name = name.split()[0].lower()
        last_name = name.split()[1].lower()
        
        return f"""══════════════════════════════════════════════════════════

{name}

📧 {first_name}.{last_name}@gmail.com | 📞 (555) {random.randint(200, 999)}-{random.randint(1000, 9999)} | 🌍 {city} | 💼 linkedin.com/in/{first_name}-{last_name}

══════════════════════════════════════════════════════════"""
    
    def generate_professional_summary(self, job_analysis: Dict, industry: str, is_matching: bool = True) -> str:
        """Generate compelling professional summary"""
        industry_data = self.industry_mappings[industry]
        must_haves = self.extract_requirements_list(job_analysis.get('must_have', []))
        
        prompt = f"""
        Create a compelling 3-4 sentence professional summary for a {industry} professional.
        
        Job requirements: {job_analysis.get('must_have', [])}
        Industry: {industry}
        Candidate quality: {"Excellent match" if is_matching else "Poor match"}
        
        Requirements:
        1. Start with years of experience (8-15 years for matching, 2-5 for non-matching)
        2. Include 2-3 specific quantified achievements with exact numbers
        3. {"Mention key technologies from requirements" if is_matching else f"Mention {industry} technologies but AVOID most job requirements"}
        4. Include industry metrics like: {', '.join(industry_data['metrics'])}
        5. End with career objective
        
        Example format:
        "Results-driven [industry] professional with [X] years of experience in [specific domains]. [Specific achievement with exact metrics]. Expert in [key technologies]. Proven track record of [achievement with numbers]. Seeking to leverage [skills] to drive [business outcome] at [company type]."
        
        Make it specific and impressive{"" if is_matching else f"""
        
        CRITICAL: For non-matching candidates in {industry}, they should LACK most required skills from: {must_haves}
        
        EXAMPLES OF WHAT TO DO (non-matching):
        - If job needs Python/ML/PhD → Write about: "3 years experience using Excel and basic SQL queries. Familiar with data visualization through Excel charts and Power BI. Bachelor's degree in Business Administration."
        - If job needs React/Node.js/5+ years → Write about: "2 years experience with basic HTML/CSS and WordPress. Some exposure to JavaScript but no framework experience. Associate's degree in Web Design."  
        - If job needs Advanced SQL/Cloud/Statistics → Write about: "3 years experience with basic database queries and Excel pivot tables. Limited exposure to statistical concepts through online courses."
        
        EXAMPLES OF WHAT NOT TO DO (don't write these for non-matching):
        - "Expert in Python and machine learning with 8 years experience"
        - "Proficient in React, Node.js, and modern JavaScript frameworks"  
        - "Advanced statistical analysis and cloud platform expertise"
        """}.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a professional resume writer. {'Create compelling summaries for excellent candidates' if is_matching else 'Create summaries for candidates who LACK most required skills - they should NOT be strong matches'}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        
        return f"""💼 PROFESSIONAL SUMMARY

{summary}

══════════════════════════════════════════════════════════"""
    
    def generate_skills_section(self, job_analysis: Dict, industry: str, is_matching: bool = True) -> str:
        """Generate detailed skills section"""
        industry_data = self.industry_mappings[industry]
        must_haves = self.extract_requirements_list(job_analysis.get('must_have', []))
        nice_to_haves = self.extract_requirements_list(job_analysis.get('nice_to_have', []))
        
        prompt = f"""
        Create a CONSISTENTLY formatted technical skills section for a {industry} professional.
        
        Must-have skills to include: {must_haves}
        Nice-to-have skills to include: {nice_to_haves}
        Industry focus areas: {industry_data['focus_areas']}
        Candidate match level: {"Excellent" if is_matching else "Poor"}
        
        CRITICAL FORMATTING REQUIREMENTS:
        1. Use ONLY simple bullet points (•) - NO NUMBERS, NO SUB-BULLETS
        2. Each category should have exactly one line with comma-separated skills
        3. Include specific versions where relevant (e.g., "React 18.2, Node.js 16.14")
        4. {"Include ALL must-have technical skills and most nice-to-have skills" if is_matching else f"""CRITICAL: EXCLUDE most must-have skills from this list: {must_haves}. Include ONLY 1-2 maximum.
        
        EXAMPLES OF WHAT TO DO (non-matching skills):
        - If job needs Python/ML/TensorFlow → Include: Excel, Power BI, basic SQL, SPSS
        - If job needs React/Node.js/AWS → Include: HTML/CSS, WordPress, basic JavaScript, Photoshop  
        - If job needs Advanced Analytics/R/Statistics → Include: Excel pivot tables, Google Analytics, basic reporting
        
        EXAMPLES OF WHAT NOT TO DO (don't include these if they're in must-haves):
        - Python, TensorFlow, PyTorch, Scikit-learn, Advanced ML algorithms
        - React, Node.js, AWS, Docker, Kubernetes, TypeScript
        - R, Advanced Statistics, Hypothesis Testing, Statistical Modeling
        """}
        5. ONLY list actual technical skills, tools, and technologies - NO experience years, NO degree requirements, NO certifications
        6. Focus on concrete technologies like programming languages, frameworks, databases, tools
        5. ONLY list actual technical skills, tools, and technologies - NO experience years, NO degree requirements, NO certifications
        6. Focus on concrete technologies like programming languages, frameworks, databases, tools
        
        EXACT FORMAT TO FOLLOW:
        {industry_data['focus_areas'][0]}: JavaScript, React 18.2, Node.js 16.14, Express.js, TypeScript
        {industry_data['focus_areas'][1]}: PostgreSQL, MySQL, MongoDB, Redis, SQL optimization  
        {industry_data['focus_areas'][2]}: REST APIs, GraphQL, Microservices, Docker, Kubernetes
        Additional Skills: AWS, Git, Jenkins, Jest, Webpack
        
        DO NOT include: years of experience, degree requirements, certifications, soft skills, or job requirements.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a professional resume writer specializing in technical skills sections. {'Include all required skills for excellent candidates' if is_matching else 'EXCLUDE most required skills for candidates who are NOT qualified - include only 1-2 required skills maximum'}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        skills_content = response.choices[0].message.content.strip()
        
        # Add bullet points to each skill line
        formatted_skills = []
        for line in skills_content.split('\n'):
            if line.strip() and ':' in line:
                formatted_skills.append(f"• {line.strip()}")
            elif line.strip():
                formatted_skills.append(line.strip())
        
        return f"""🛠️ TECHNICAL EXPERTISE

{chr(10).join(formatted_skills)}

══════════════════════════════════════════════════════════"""
    
    def extract_requirements_list(self, requirements):
        """Helper method to convert requirements to list format"""
        if isinstance(requirements, dict):
            return list(requirements.values())
        elif isinstance(requirements, list):
            return requirements
        else:
            return []
    
    def generate_work_experience(self, job_analysis: Dict, industry: str, position_level: str, is_matching: bool = True) -> str:
        """Generate detailed work experience for a single position"""
        industry_data = self.industry_mappings[industry]
        must_haves = self.extract_requirements_list(job_analysis.get('must_have', []))
        
        # For non-matching candidates, stay in same industry but avoid must-have requirements
        companies = industry_data['companies']
        achievements = industry_data['achievements'] 
        work_industry = industry
        
        prompt = f"""
        Create a detailed work experience entry for a {position_level} {work_industry} professional.
        
        Target job industry: {industry}
        Candidate's actual industry: {work_industry}
        Must-have skills required: {must_haves}
        Skills to demonstrate: {must_haves if is_matching else f"Some {industry} skills but missing most must-haves: {must_haves}"}
        Position level: {position_level} (Senior, Mid-level, or Junior)
        Candidate quality: {"Excellent match" if is_matching else f"Poor match - same {industry} industry but lacks most required skills"}
        Available companies: {companies}
        Achievement templates: {achievements}
        
        Generate ONE job entry with this EXACT format:
        
        Company Name - Job Title
        Start Date - End Date | City, State
        
        IMPORTANT: 
        - Use DIFFERENT company from the available companies list for each job entry
        - Use logical date progression based on position level:
          * Senior: January 2022 - Present, March 2021 - Present, etc.
          * Mid-level: June 2019 - December 2021, August 2018 - February 2021, etc. 
          * Junior: May 2016 - May 2019, September 2017 - July 2019, etc.
        - Each position should be at a DIFFERENT company
        - No overlapping or identical date ranges
        
        • [bullet point 1]
        • [bullet point 2]
        • [bullet point 3]
        • [bullet point 4]
        • [bullet point 5]
        • [bullet point 6]
        
        CRITICAL FORMATTING REQUIREMENTS:
        1. Use ONLY simple bullet points (•) - NO NUMBERS, NO DASHES, NO SUB-BULLETS
        2. Start each bullet with a power action verb (Architected, Developed, Led, Optimized, Implemented, Collaborated)
        3. Include specific technology/methodology used
        4. Include quantified business impact with exact numbers
        5. {"Show expertise in required skills" if is_matching else f"""Show {industry} experience but AVOID most must-have skills from: {must_haves}
        
        EXAMPLES OF WHAT TO DO (non-matching work experience):
        - If job needs Python/ML → Write: "Analyzed data using Excel pivot tables and basic SQL queries. Created simple reports using Power BI dashboard tools."
        - If job needs React/AWS → Write: "Developed basic websites using HTML/CSS and WordPress. Updated content management systems and handled simple JavaScript tasks."
        - If job needs Advanced Statistics → Write: "Performed basic data analysis using Excel functions. Generated standard reports and identified simple trends in datasets."
        
        EXAMPLES OF WHAT NOT TO DO (don't write these for non-matching):
        - "Implemented machine learning algorithms using Python and TensorFlow"
        - "Architected React applications with Node.js backend on AWS infrastructure"  
        - "Conducted advanced statistical modeling and hypothesis testing"
        """}
        
        
        Examples of correct format for matching candidates:
        • Architected microservices platform using React 18 and Node.js 16, serving 2.3M daily users with 99.9% uptime
        • Led team of 5 developers to migrate legacy system to AWS, reducing infrastructure costs by $150K annually
        • Optimized PostgreSQL database queries reducing response time from 800ms to 180ms, improving user satisfaction by 35%
        
        CRITICAL DATE AND COMPANY EXAMPLES:
        
        CORRECT date progression (most recent first):
        - Senior Role: January 2022 - Present | Company A
        - Mid Role: March 2020 - December 2021 | Company B  
        - Junior Role: June 2018 - February 2020 | Company C
        
        WRONG date examples (DON'T do this):
        - All same dates: "January 2020 - Present" for every job
        - Overlapping dates: Job A ends 2021, Job B starts 2020
        - Future dates or impossible timelines
        
        COMPANY VARIETY EXAMPLES (use different companies from the list):
        - If data science: DataInsights Corp, Analytics Pro, ML Solutions Inc., PredictiveEdge, Intelligence Systems
        - If technology: TechCorp, InnovateSoft, DataFlow Systems, CloudTech Solutions, DevTools Inc.
        - If marketing: BrandBoost Marketing, DigitalEdge Agency, MarketPro Solutions, Creative Campaigns Inc.
        
        Use realistic dates (2016-2024), specific numbers, and concrete technical details.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a professional resume writer specializing in {industry} roles. {'Create strong experience entries for excellent candidates' if is_matching else 'Create experience entries for candidates who LACK most required qualifications - they should NOT demonstrate proficiency in most job requirements'}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        
        work_content = response.choices[0].message.content.strip()
        
        # Add emojis and ensure consistent formatting
        formatted_lines = []
        lines = work_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            if ' - ' in line and not line.startswith('•') and not line.startswith('-') and not line.startswith('🏢'):
                # This is a company-title line
                formatted_lines.append(f"🏢 {line}")
            elif '|' in line and any(year in line for year in ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']):
                # This is a date-location line  
                formatted_lines.append(f"📅 {line}")
            elif line.startswith('•'):
                # Already properly formatted bullet point
                formatted_lines.append(line)
            elif line.startswith('-') or line.startswith('*'):
                # Convert dashes or asterisks to bullet points
                cleaned_line = line.lstrip('-*').strip()
                formatted_lines.append(f"• {cleaned_line}")
            elif line and not line.startswith('🏢') and not line.startswith('📅'):
                # Regular text line
                formatted_lines.append(line)
        
        return chr(10).join(formatted_lines)
    
    def generate_education_certifications(self, job_analysis: Dict, industry: str, is_matching: bool = True) -> str:
        """Generate education and certifications section"""
        prompt = f"""
        Create education and certifications section for a {industry} professional.
        
        Job requirements: {job_analysis.get('must_have', [])}
        Industry: {industry}
        Candidate quality: {"Excellent match" if is_matching else "Poor match"}
        
        Generate:
        1. Relevant degree for {industry}
        2. Realistic university name
        3. Graduation year (2012-2018 for experienced professional)
        4. {"2-3 relevant certifications with exact dates" if is_matching else "0-1 basic certification"}
        5. {"Relevant coursework if applicable" if is_matching else "Basic information only"}
        
        {"" if is_matching else f"""
        EXAMPLES FOR NON-MATCHING EDUCATION:
        - If job needs PhD/Master's in Statistics/CS → Include: Bachelor's in Business, Communications, or General Studies
        - If job needs Computer Science degree → Include: Associate's degree or certification program  
        - If job needs Advanced certifications → Include: Basic online course completion or no certifications
        
        EXAMPLES OF WHAT NOT TO DO (don't include if job requires these):
        - Don't include PhD/Master's if job requires advanced degree
        - Don't include Computer Science/Engineering degrees if job requires technical degree
        - Don't include multiple relevant certifications if job values certifications
        """}
        
        CRITICAL FORMATTING REQUIREMENTS:
        1. Use ONLY simple bullet points (•) for certifications - NO DASHES, NO NUMBERS
        2. Keep coursework on single line with simple format
        3. Use consistent date formatting
        
        EXACT FORMAT TO FOLLOW:
        EDUCATION
        
        Degree in Field
        University Name | Graduation Year
        {"Relevant Coursework: [specific courses]" if is_matching else ""}
        
        CERTIFICATIONS
        
        • Certification Name - Organization (Year)
        {"• Second Certification - Organization (Year)" if is_matching else ""}
        
        Use realistic certification names for {industry} and recent dates (2020-2024).
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a professional resume writer specializing in {industry} education and certifications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        
        edu_content = response.choices[0].message.content.strip()
        
        # Add emojis to education section
        formatted_lines = []
        in_education = False
        in_certifications = False
        
        for line in edu_content.split('\n'):
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            if 'EDUCATION' in line.upper():
                formatted_lines.append(f"🎓 EDUCATION & CERTIFICATIONS")
                in_education = True
                formatted_lines.append('')
                continue
            elif 'CERTIFICATIONS' in line.upper():
                formatted_lines.append('')
                formatted_lines.append("🏅 CERTIFICATIONS (Recent & Relevant)")
                in_certifications = True
                continue
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                # Certification item - standardize to bullet points
                cleaned_line = line.lstrip('-•*').strip()
                formatted_lines.append(f"• {cleaned_line}")
            elif '|' in line and in_education:
                # University line
                formatted_lines.append(f"🎓 {line}")
            elif in_education and any(word in line for word in ['Bachelor', 'Master', 'PhD', 'Degree']):
                # Degree line
                formatted_lines.append(f"🎓 {line}")
            elif in_education and ('Coursework' in line or 'Project' in line):
                # Coursework or project line
                formatted_lines.append(f"📚 {line}")
            else:
                formatted_lines.append(line)
        
        result = chr(10).join(formatted_lines)
        
        # Add bottom separator
        if not result.endswith('══════════════════════════════════════════════════════════'):
            result += f"\n\n══════════════════════════════════════════════════════════"
        
        return result
    
    def assemble_multi_stage_resume(self, job_analysis: Dict, is_matching: bool = True) -> str:
        """Assemble resume using multi-stage generation approach"""
        industry = self.classify_industry(job_analysis)
        
        # Generate each section separately
        contact_info = self.generate_contact_info(is_matching)
        summary = self.generate_professional_summary(job_analysis, industry, is_matching)
        skills = self.generate_skills_section(job_analysis, industry, is_matching)
        
        # Generate 3 work experience entries
        senior_experience = self.generate_work_experience(job_analysis, industry, "Senior", is_matching)
        mid_experience = self.generate_work_experience(job_analysis, industry, "Mid-level", is_matching)  
        junior_experience = self.generate_work_experience(job_analysis, industry, "Junior", is_matching)
        
        education_certs = self.generate_education_certifications(job_analysis, industry, is_matching)
        
        # Assemble final resume with proper formatting
        resume = f"""{contact_info}

{summary}

{skills}

💼 PROFESSIONAL EXPERIENCE

{senior_experience}

{mid_experience}

{junior_experience}

{education_certs}"""
        
        return resume
    
    
    def parse_job_description(self, job_description: str) -> Dict:
        prompt = f"""
        Analyze the following job description and extract key information.
        
        Job Description:
        {job_description}
        
        Extract and return ONLY a valid JSON object with these exact keys:
        - "must_have": array of strings containing hard requirements/qualifications
        - "nice_to_have": array of strings containing preferred qualifications  
        - "job_title": string with the job title
        - "industry": string describing the industry/domain
        - "responsibilities": array of strings with key responsibilities
        
        Example format:
        {{
          "must_have": ["5+ years Python experience", "Django/Flask frameworks", "SQL databases"],
          "nice_to_have": ["AWS experience", "Docker knowledge"],
          "job_title": "Senior Software Engineer",
          "industry": "Technology/Software",
          "responsibilities": ["Develop web applications", "Build APIs"]
        }}
        
        Return ONLY the JSON object, no other text.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a job description analyst. Extract key requirements and return them in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        try:
            content = response.choices[0].message.content.strip()
            # Try to extract JSON if it's wrapped in markdown code blocks
            if content.startswith('```json'):
                content = content.split('```json')[1].split('```')[0].strip()
            elif content.startswith('```'):
                content = content.split('```')[1].split('```')[0].strip()
            
            return json.loads(content)
        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            print(f"Warning: Failed to parse job description JSON: {e}")
            print(f"Raw response: {response.choices[0].message.content}")
            return {
                "must_have": [],
                "nice_to_have": [],
                "job_title": "Unknown",
                "industry": "Unknown", 
                "responsibilities": []
            }
    
    def generate_matching_resume(self, job_analysis: Dict) -> str:
        return self.assemble_multi_stage_resume(job_analysis, is_matching=True)
    
    def generate_non_matching_resume(self, job_analysis: Dict) -> str:
        return self.assemble_multi_stage_resume(job_analysis, is_matching=False)
    
    def generate_resumes(self, job_description: str) -> Tuple[str, str]:
        job_analysis = self.parse_job_description(job_description)
        matching_resume = self.generate_matching_resume(job_analysis)
        non_matching_resume = self.generate_non_matching_resume(job_analysis)
        
        return matching_resume, non_matching_resume
    
    def generate_resumes_txt(self, job_description: str, output_dir: str = "output"):
        """Generate TXT resume files with full emoji formatting"""
        matching_resume, non_matching_resume = self.generate_resumes(job_description)
        
        os.makedirs(output_dir, exist_ok=True)
        
        matching_txt = os.path.join(output_dir, 'matching_resume.txt')
        non_matching_txt = os.path.join(output_dir, 'non_matching_resume.txt')
        
        # Write TXT files with UTF-8 encoding to preserve emojis
        with open(matching_txt, 'w', encoding='utf-8') as f:
            f.write(matching_resume)
            
        with open(non_matching_txt, 'w', encoding='utf-8') as f:
            f.write(non_matching_resume)
        
        return matching_txt, non_matching_txt
    
    def generate_resumes_pdf(self, job_description: str, output_dir: str = "output"):
        """Generate PDF resume files (legacy method)"""
        matching_resume, non_matching_resume = self.generate_resumes(job_description)
        
        os.makedirs(output_dir, exist_ok=True)
        
        matching_pdf = os.path.join(output_dir, 'matching_resume.pdf')
        non_matching_pdf = os.path.join(output_dir, 'non_matching_resume.pdf')
        
        self.pdf_generator.create_pdf_resume(matching_resume, matching_pdf)
        self.pdf_generator.create_pdf_resume(non_matching_resume, non_matching_pdf)
        
        return matching_pdf, non_matching_pdf