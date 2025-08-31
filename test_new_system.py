#!/usr/bin/env python3

"""
Test script to verify the new dynamic resume generation system
"""

from resume_generator import ResumeGenerator
import json

def test_resume_generation():
    print("🧪 Testing New Dynamic Resume Generation System")
    print("=" * 60)
    
    # Initialize generator
    generator = ResumeGenerator()
    
    # Test job analysis for a marketing position
    test_job_analysis = {
        "job_title": "Digital Marketing Manager", 
        "industry": "Digital Marketing",
        "must_have": [
            "4+ years digital marketing experience",
            "Google Ads and Facebook Ads certification", 
            "Analytics tools proficiency (Google Analytics, SEMrush)",
            "Content management system experience",
            "Email marketing campaign management"
        ],
        "nice_to_have": [
            "HubSpot CRM experience",
            "Salesforce knowledge", 
            "Video editing skills (Adobe Premiere)",
            "SEO/SEM advanced techniques",
            "Marketing automation tools"
        ]
    }
    
    print("📋 Test Job Analysis:")
    print(f"   Title: {test_job_analysis['job_title']}")
    print(f"   Industry: {test_job_analysis['industry']}")
    print(f"   Must-haves: {len(test_job_analysis['must_have'])}")
    print(f"   Nice-to-haves: {len(test_job_analysis['nice_to_have'])}")
    print()
    
    # Test industry classification
    classified_industry = generator.classify_industry(test_job_analysis)
    print(f"🎯 Classified Industry: {classified_industry}")
    print()
    
    # Generate matching resume
    print("📝 Generating matching resume...")
    matching_resume = generator.generate_matching_resume(test_job_analysis)
    
    print("✅ Matching Resume Generated!")
    print("Preview (first 500 characters):")
    print("-" * 40)
    print(matching_resume[:500] + "...")
    print("-" * 40)
    print()
    
    # Generate non-matching resume
    print("📝 Generating non-matching resume...")
    non_matching_resume = generator.generate_non_matching_resume(test_job_analysis)
    
    print("✅ Non-Matching Resume Generated!")
    print("Preview (first 500 characters):")
    print("-" * 40)
    print(non_matching_resume[:500] + "...")
    print("-" * 40)
    print()
    
    print("🎉 Test completed successfully!")
    
    # Save test results as formatted TXT files
    import os
    os.makedirs('test_output', exist_ok=True)
    
    matching_txt = 'test_output/new_system_matching.txt'
    non_matching_txt = 'test_output/new_system_non_matching.txt'
    
    with open(matching_txt, 'w', encoding='utf-8') as f:
        f.write(matching_resume)
        
    with open(non_matching_txt, 'w', encoding='utf-8') as f:
        f.write(non_matching_resume)
    
    print(f"📁 Matching resume saved to: {matching_txt}")
    print(f"📁 Non-matching resume saved to: {non_matching_txt}")

if __name__ == "__main__":
    test_resume_generation()