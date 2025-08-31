#!/usr/bin/env python3
"""
Test TXT file generation with beautiful emoji formatting
"""

import os
from resume_generator import ResumeGenerator

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        exit(1)
    
    # Simple test job
    test_job = """
    Senior Full-Stack Developer Position
    
    MUST-HAVE REQUIREMENTS:
    - 5+ years of JavaScript development experience
    - Expert-level React.js and Node.js skills
    - Strong SQL database experience
    
    NICE-TO-HAVE REQUIREMENTS:
    - AWS cloud platform experience
    - Docker containerization knowledge
    
    Company: TechStartup Inc.
    Industry: Software Technology
    """
    
    generator = ResumeGenerator()
    
    print("🧪 TESTING TXT FILE GENERATION WITH EMOJI FORMATTING")
    print("=" * 70)
    
    try:
        # Generate TXT files
        matching_txt, non_matching_txt = generator.generate_resumes_txt(test_job, 'txt_output')
        
        print(f"✅ TXT Files Generated:")
        print(f"   📄 Matching: {matching_txt}")
        print(f"   📄 Non-matching: {non_matching_txt}")
        print("\n✨ These TXT files preserve all the beautiful emoji formatting!")
        print("📋 Compare these files to detailed_marketing_resume.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")