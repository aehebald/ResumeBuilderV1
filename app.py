#!/usr/bin/env python3
"""
Beautiful Web Application for Resume Generator
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import json
from resume_generator import ResumeGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def index():
    """Main page with job posting input form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resumes():
    """API endpoint to generate resumes"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({'error': 'OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable.'}), 500
        
        # Generate resumes
        generator = ResumeGenerator()
        
        # Create temporary directory for outputs
        with tempfile.TemporaryDirectory() as temp_dir:
            matching_txt, non_matching_txt = generator.generate_resumes_txt(job_description, temp_dir)
            
            # Read the generated files
            with open(matching_txt, 'r', encoding='utf-8') as f:
                good_resume = f.read()
            
            with open(non_matching_txt, 'r', encoding='utf-8') as f:
                bad_resume = f.read()
        
        return jsonify({
            'good_resume': good_resume,
            'bad_resume': bad_resume,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    """Export resumes as PDF files"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        generator = ResumeGenerator()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            matching_pdf, non_matching_pdf = generator.generate_resumes_pdf(job_description, temp_dir)
            
            # Read PDF files as base64
            import base64
            with open(matching_pdf, 'rb') as f:
                good_pdf_data = base64.b64encode(f.read()).decode()
            
            with open(non_matching_pdf, 'rb') as f:
                bad_pdf_data = base64.b64encode(f.read()).decode()
        
        return jsonify({
            'good_pdf': good_pdf_data,
            'bad_pdf': bad_pdf_data,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': f'PDF export failed: {str(e)}'}), 500

@app.route('/analyze-requirement', methods=['POST'])
def analyze_requirement():
    """Analyze if a resume meets a specific requirement using AI"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '').strip()
        resume_text = data.get('resume_text', '').strip()
        
        if not requirement or not resume_text:
            return jsonify({'error': 'Both requirement and resume text are required'}), 400
        
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        prompt = f"""
Analyze if the following resume meets the specific requirement. Return a JSON response with:
1. "meets_requirement": true/false
2. "explanation": Brief factual explanation (1-2 sentences)
3. "evidence": Specific text from the resume that supports your decision (or lack thereof)

Requirement: {requirement}

Resume:
{resume_text}

Be strict in your evaluation. Only return true if the requirement is clearly and explicitly met.
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        # Parse the AI response
        ai_response = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            # Fallback parsing if AI doesn't return proper JSON
            meets = 'true' in ai_response.lower() and 'meets_requirement' in ai_response.lower()
            result = {
                'meets_requirement': meets,
                'explanation': ai_response[:200] + '...' if len(ai_response) > 200 else ai_response,
                'evidence': 'See full analysis above'
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set it in your deployment platform's environment variables")
    
    # Use PORT from environment (Railway/Heroku) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    print("🚀 Starting Resume AI Generator Web App...")
    print(f"🌐 App will be available on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)