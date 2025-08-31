#!/usr/bin/env python3

from resume_generator import ResumeGenerator
import os

def test_detailed_resume():
    print("🧪 Testing Dramatically Improved Resume Generation")
    print("=" * 60)
    
    generator = ResumeGenerator()
    
    # Test with a marketing job analysis
    marketing_analysis = {
        'job_title': 'Digital Marketing Manager',
        'industry': 'Digital Marketing', 
        'must_have': [
            '5+ years digital marketing experience',
            'Google Ads and Facebook Ads certification',
            'Analytics tools (Google Analytics, SEMrush)',
            'Email marketing campaigns',
            'Content management systems'
        ],
        'nice_to_have': [
            'HubSpot CRM experience',
            'Video editing (Adobe Premiere)',
            'SEO/SEM techniques',
            'A/B testing',
            'Marketing automation'
        ]
    }
    
    print("📋 Generating detailed marketing resume...")
    resume = generator.generate_matching_resume(marketing_analysis)
    
    print("✅ Resume Generated!")
    print("=" * 60)
    print(resume)
    print("=" * 60)
    
    # Save to file
    with open('detailed_marketing_resume.txt', 'w', encoding='utf-8') as f:
        f.write(resume)
    
    print("\n📁 Complete resume saved to: detailed_marketing_resume.txt")
    
    # Also test a tech resume
    print("\n📋 Generating detailed tech resume...")
    tech_analysis = {
        'job_title': 'Senior Software Engineer',
        'industry': 'Software Technology',
        'must_have': [
            '7+ years Python development',
            'React and Node.js experience', 
            'PostgreSQL databases',
            'REST API development',
            'Git version control'
        ],
        'nice_to_have': [
            'AWS cloud platform',
            'Docker containerization',
            'GraphQL APIs',
            'CI/CD pipelines',
            'Microservices architecture'
        ]
    }
    
    tech_resume = generator.generate_matching_resume(tech_analysis)
    
    with open('detailed_tech_resume.txt', 'w', encoding='utf-8') as f:
        f.write(tech_resume)
        
    print("✅ Tech resume saved to: detailed_tech_resume.txt")
    print("\n🎉 Test completed! Check the generated files for full detailed resumes.")

if __name__ == "__main__":
    test_detailed_resume()