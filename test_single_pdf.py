#!/usr/bin/env python3
"""
Test single TXT generation with improved formatting
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
    
    print("🧪 TESTING SINGLE TXT GENERATION WITH IMPROVED FORMATTING")
    print("=" * 70)
    
    try:
        # Generate just the matching TXT
        matching_txt, _ = generator.generate_resumes_txt(test_job, 'test_single_output')
        
        print(f"✅ TXT Generated: {matching_txt}")
        print("\n📋 This TXT file has all the beautiful emoji formatting!")
        print("✨ Compare this to detailed_marketing_resume.txt to see the improved formatting")
        
    except Exception as e:
        print(f"❌ Error: {e}")