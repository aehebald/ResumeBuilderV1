#!/usr/bin/env python3
"""
Simple test script for the resume generator
"""

import os
from resume_generator import ResumeGenerator

def test_with_sample_job():
    if not os.getenv('OPENAI_API_KEY'):
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Sample job description
    job_description = """
    Data Scientist Position
    
    Must-have requirements:
    - PhD or Master's in Data Science, Statistics, or related field
    - 3+ years experience in machine learning
    - Proficiency in Python and R
    - Experience with SQL and databases
    - Knowledge of statistical analysis
    
    Nice-to-have:
    - Experience with AWS/GCP
    - Knowledge of deep learning frameworks (TensorFlow, PyTorch)
    - Experience with big data tools (Spark, Hadoop)
    """
    
    print("Testing resume generator with sample job description...")
    
    generator = ResumeGenerator()
    
    print("Analyzing job description...")
    job_analysis = generator.parse_job_description(job_description)
    print(f"Job Analysis: {job_analysis}")
    
    print("\nGenerating matching resume...")
    matching_resume = generator.generate_matching_resume(job_analysis)
    print("Matching resume generated!")
    
    print("\nGenerating non-matching resume...")
    non_matching_resume = generator.generate_non_matching_resume(job_analysis)
    print("Non-matching resume generated!")
    
    # Generate TXT files with proper formatting
    print("\nGenerating formatted TXT files...")
    matching_txt, non_matching_txt = generator.generate_resumes_txt(job_description, 'test_output')
    
    # Save job analysis
    os.makedirs('test_output', exist_ok=True)
    with open('test_output/job_analysis.txt', 'w', encoding='utf-8') as f:
        f.write(str(job_analysis))
    
    print(f"✅ Test completed! Generated files:")
    print(f"   📄 Matching resume: {matching_txt}")
    print(f"   📄 Non-matching resume: {non_matching_txt}")
    print(f"   📊 Job analysis: test_output/job_analysis.txt")

if __name__ == '__main__':
    test_with_sample_job()