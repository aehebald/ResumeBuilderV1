#!/usr/bin/env python3
"""
Resume Generator - Creates matching and non-matching resumes based on job descriptions
"""

import argparse
import os
from resume_generator import ResumeGenerator

def save_resume(resume_content: str, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(resume_content)
    print(f"Resume saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate matching and non-matching resumes from job descriptions')
    parser.add_argument('--job-file', '-f', help='Path to file containing job description')
    parser.add_argument('--job-text', '-t', help='Job description text directly')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory for resumes')
    parser.add_argument('--format', choices=['txt', 'pdf'], default='txt', help='Output format (txt or pdf)')
    
    args = parser.parse_args()
    
    if not args.job_file and not args.job_text:
        print("Please provide either --job-file or --job-text")
        return
    
    if not os.getenv('OPENAI_API_KEY'):
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Get job description
    if args.job_file:
        with open(args.job_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
    else:
        job_description = args.job_text
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate resumes
    print("Generating resumes...")
    generator = ResumeGenerator()
    
    if args.format == 'pdf':
        matching_pdf, non_matching_pdf = generator.generate_resumes_pdf(job_description, args.output_dir)
        print(f"PDF resumes saved to:")
        print(f"  Matching: {matching_pdf}")
        print(f"  Non-matching: {non_matching_pdf}")
    else:
        # Use the new TXT generation method for beautiful formatting
        matching_txt, non_matching_txt = generator.generate_resumes_txt(job_description, args.output_dir)
        print(f"TXT resumes with emoji formatting saved to:")
        print(f"  Matching: {matching_txt}")
        print(f"  Non-matching: {non_matching_txt}")
    
    print("Resume generation completed!")

if __name__ == '__main__':
    main()