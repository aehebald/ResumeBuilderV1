#!/usr/bin/env python3
"""
Test script to verify ChatGPT API integration with must-haves and nice-to-haves
"""

import os
import json
from resume_generator import ResumeGenerator

def get_requirements_safely(analysis, key):
    """Helper function to safely extract requirements from either dict or list format"""
    requirements = analysis.get(key, [])
    if isinstance(requirements, dict):
        return list(requirements.values())
    return requirements

def get_requirements_count(analysis, key):
    """Helper function to safely count requirements"""
    requirements = analysis.get(key, [])
    return len(requirements) if isinstance(requirements, (list, dict)) else 0

def test_api_with_different_requirements():
    """Test the API with different job requirements scenarios"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    # Test case 1: Tech job with clear must-haves and nice-to-haves
    tech_job = """
    Senior Full-Stack Developer Position
    
    MUST-HAVE REQUIREMENTS (Required):
    - 5+ years of JavaScript development experience
    - Expert-level React.js and Node.js skills
    - Strong SQL database experience (PostgreSQL/MySQL)
    - RESTful API design and development
    - Git version control proficiency
    - Bachelor's degree in Computer Science or equivalent experience
    
    NICE-TO-HAVE REQUIREMENTS (Preferred):
    - AWS cloud platform experience
    - Docker containerization knowledge
    - TypeScript experience
    - GraphQL API development
    - CI/CD pipeline setup (Jenkins/GitHub Actions)
    - Agile/Scrum methodology experience
    - Microservices architecture knowledge
    
    Company: TechStartup Inc.
    Industry: Software Technology
    Location: Remote
    """
    
    # Test case 2: Marketing job with different requirements
    marketing_job = """
    Digital Marketing Manager Position
    
    MUST-HAVE REQUIREMENTS (Required):
    - 4+ years digital marketing experience
    - Google Ads and Facebook Ads certification
    - Analytics tools proficiency (Google Analytics, SEMrush)
    - Content management system experience
    - Email marketing campaign management
    - Bachelor's degree in Marketing or related field
    
    NICE-TO-HAVE REQUIREMENTS (Preferred):
    - HubSpot CRM experience
    - Salesforce knowledge
    - Video editing skills (Adobe Premiere)
    - SEO/SEM advanced techniques
    - Marketing automation tools
    - Social media influencer partnerships
    - A/B testing experience
    
    Company: BrandGrow Agency
    Industry: Digital Marketing
    Location: New York, NY
    """
    
    generator = ResumeGenerator()
    os.makedirs('api_test_output', exist_ok=True)
    
    print("🚀 TESTING CHATGPT API WITH DIFFERENT JOB REQUIREMENTS")
    print("=" * 70)
    
    # Test 1: Tech Job
    print("\n📋 TEST 1: TECH JOB (JavaScript/React)")
    print("-" * 50)
    print("Testing job requirements parsing...")
    
    try:
        tech_analysis = generator.parse_job_description(tech_job)
        print("✅ Job analysis completed!")
        print(f"   Must-haves found: {get_requirements_count(tech_analysis, 'must_have')}")
        print(f"   Nice-to-haves found: {get_requirements_count(tech_analysis, 'nice_to_have')}")
        print(f"   Job title: {tech_analysis.get('job_title', 'Unknown')}")
        
        print("\n🔍 PARSED REQUIREMENTS:")
        must_haves = get_requirements_safely(tech_analysis, 'must_have')
        nice_to_haves = get_requirements_safely(tech_analysis, 'nice_to_have')
        print("Must-haves:", must_haves[:3], "..." if len(must_haves) > 3 else "")
        print("Nice-to-haves:", nice_to_haves[:3], "..." if len(nice_to_haves) > 3 else "")
        
        print("\n📝 Generating resumes...")
        tech_matching_txt, tech_non_matching_txt = generator.generate_resumes_txt(
            tech_job, 'api_test_output/tech_job'
        )
        
        print(f"✅ Tech job TXT files generated:")
        print(f"   📄 Matching: {tech_matching_txt}")
        print(f"   📄 Non-matching: {tech_non_matching_txt}")
        
    except Exception as e:
        print(f"❌ Tech job test failed: {str(e)}")
    
    # Test 2: Marketing Job  
    print("\n📋 TEST 2: MARKETING JOB (Digital Marketing)")
    print("-" * 50)
    print("Testing job requirements parsing...")
    
    try:
        marketing_analysis = generator.parse_job_description(marketing_job)
        print("✅ Job analysis completed!")
        print(f"   Must-haves found: {get_requirements_count(marketing_analysis, 'must_have')}")
        print(f"   Nice-to-haves found: {get_requirements_count(marketing_analysis, 'nice_to_have')}")
        print(f"   Job title: {marketing_analysis.get('job_title', 'Unknown')}")
        
        print("\n🔍 PARSED REQUIREMENTS:")
        must_haves = get_requirements_safely(marketing_analysis, 'must_have')
        nice_to_haves = get_requirements_safely(marketing_analysis, 'nice_to_have')
        print("Must-haves:", must_haves[:3], "..." if len(must_haves) > 3 else "")
        print("Nice-to-haves:", nice_to_haves[:3], "..." if len(nice_to_haves) > 3 else "")
        
        print("\n📝 Generating resumes...")
        marketing_matching_txt, marketing_non_matching_txt = generator.generate_resumes_txt(
            marketing_job, 'api_test_output/marketing_job'
        )
        
        print(f"✅ Marketing job TXT files generated:")
        print(f"   📄 Matching: {marketing_matching_txt}")
        print(f"   📄 Non-matching: {marketing_non_matching_txt}")
        
    except Exception as e:
        print(f"❌ Marketing job test failed: {str(e)}")
    
    # Test 3: Custom requirements test
    custom_job = """
    Data Scientist Position
    
    MUST-HAVE REQUIREMENTS:
    - PhD or Master's in Statistics, Mathematics, or Computer Science
    - 3+ years Python programming experience
    - Machine Learning algorithms expertise (supervised/unsupervised)
    - Statistical analysis and hypothesis testing
    - SQL and database querying
    - Data visualization tools (matplotlib, seaborn, plotly)
    
    NICE-TO-HAVE REQUIREMENTS:
    - Deep Learning frameworks (TensorFlow, PyTorch)
    - Big Data tools (Spark, Hadoop)
    - Cloud platforms (AWS, GCP, Azure)
    - R programming language
    - MLOps and model deployment
    - Domain expertise in finance or healthcare
    
    Company: DataTech Solutions
    Industry: Data Analytics
    """
    
    print("\n📋 TEST 3: DATA SCIENCE JOB (Python/ML)")
    print("-" * 50)
    
    try:
        data_analysis = generator.parse_job_description(custom_job)
        print("✅ Job analysis completed!")
        print(f"   Must-haves found: {get_requirements_count(data_analysis, 'must_have')}")
        print(f"   Nice-to-haves found: {get_requirements_count(data_analysis, 'nice_to_have')}")
        print(f"   Job title: {data_analysis.get('job_title', 'Unknown')}")
        
        print("\n🔍 PARSED REQUIREMENTS:")
        must_haves = get_requirements_safely(data_analysis, 'must_have')
        nice_to_haves = get_requirements_safely(data_analysis, 'nice_to_have')
        print("Must-haves:", must_haves[:3], "..." if len(must_haves) > 3 else "")
        print("Nice-to-haves:", nice_to_haves[:3], "..." if len(nice_to_haves) > 3 else "")
        
        # Save detailed analysis
        with open('api_test_output/job_analyses.json', 'w') as f:
            json.dump({
                'tech_job': tech_analysis,
                'marketing_job': marketing_analysis,
                'data_science_job': data_analysis
            }, f, indent=2)
        
        print(f"✅ Job analyses saved to: api_test_output/job_analyses.json")
        
        print("\n📝 Generating data science resumes...")
        data_matching_txt, data_non_matching_txt = generator.generate_resumes_txt(
            custom_job, 'api_test_output/data_science'
        )
        
        print(f"✅ Data science TXT files generated:")
        print(f"   📄 Matching: {data_matching_txt}")
        print(f"   📄 Non-matching: {data_non_matching_txt}")
        
    except Exception as e:
        print(f"❌ Data science test failed: {str(e)}")
    
    print("\n🎉 API TESTING COMPLETED!")
    print("=" * 70)
    print("📁 Check the 'api_test_output/' directory for all generated TXT files")
    print("📊 Job requirement analyses saved in 'job_analyses.json'")

def test_requirement_extraction():
    """Test specifically how well the API extracts must-haves vs nice-to-haves"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        return
    
    test_job = """
    Software Engineering Manager
    
    MUST HAVE (Non-negotiable):
    - 7+ years software development experience
    - 3+ years team leadership experience
    - Strong background in Java or Python
    - Experience with agile methodologies
    - Bachelor's degree in Computer Science
    
    NICE TO HAVE (Preferred):
    - Master's degree in Computer Science
    - Experience with cloud platforms (AWS/Azure)
    - Knowledge of DevOps practices
    - Startup experience
    - Open source contributions
    """
    
    print("\n🔬 REQUIREMENT EXTRACTION TEST")
    print("=" * 50)
    
    generator = ResumeGenerator()
    
    try:
        analysis = generator.parse_job_description(test_job)
        
        print("📋 EXTRACTED REQUIREMENTS:")
        print(f"🔴 MUST-HAVES ({len(analysis.get('must_have', []))}):")
        for i, req in enumerate(analysis.get('must_have', []), 1):
            print(f"   {i}. {req}")
            
        print(f"\n🟢 NICE-TO-HAVES ({len(analysis.get('nice_to_have', []))}):")
        for i, req in enumerate(analysis.get('nice_to_have', []), 1):
            print(f"   {i}. {req}")
            
        print(f"\n📊 JOB DETAILS:")
        print(f"   Title: {analysis.get('job_title', 'N/A')}")
        print(f"   Industry: {analysis.get('industry', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Requirement extraction test failed: {str(e)}")

if __name__ == '__main__':
    print("🧪 CHATGPT API INTEGRATION TESTS")
    print("=" * 70)
    
    # Run main API tests
    test_api_with_different_requirements()
    
    # Run requirement extraction test
    test_requirement_extraction()