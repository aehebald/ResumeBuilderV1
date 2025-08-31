#!/usr/bin/env python3
"""
Quick test to see formatted resume text output
"""

import os
from resume_generator import ResumeGenerator

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        exit(1)
    
    # Test job
    tech_job = """
    Senior Full-Stack Developer Position
    
    MUST-HAVE REQUIREMENTS (Required):
    - 5+ years of JavaScript development experience
    - Expert-level React.js and Node.js skills
    - Strong SQL database experience (PostgreSQL/MySQL)
    
    NICE-TO-HAVE REQUIREMENTS (Preferred):
    - AWS cloud platform experience
    - Docker containerization knowledge
    - TypeScript experience
    
    Company: TechStartup Inc.
    Industry: Software Technology
    """
    
    generator = ResumeGenerator()
    
    print("🔍 TESTING FORMATTED TEXT OUTPUT")
    print("=" * 70)
    
    # Parse job
    job_analysis = generator.parse_job_description(tech_job)
    
    # Generate matching resume text
    resume_text = generator.generate_matching_resume(job_analysis)
    
    print("📝 GENERATED RESUME TEXT:")
    print("-" * 70)
    print(resume_text)
    print("-" * 70)
    
    # Save to file for inspection
    with open('test_formatted_output.txt', 'w', encoding='utf-8') as f:
        f.write(resume_text)
    
    print("\n✅ Resume text saved to: test_formatted_output.txt")