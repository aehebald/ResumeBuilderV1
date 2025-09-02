# AI Role Requirements Assistant

A powerful web application for HR professionals and recruiters to generate realistic resume examples (both good and bad) based on job requirements. Uses AI to create training examples for resume screening.

## 🚀 Features

- **Smart Requirements Input**: Separate non-negotiables from nice-to-haves
- **AI-Powered Analysis**: Uses OpenAI to analyze if resumes meet requirements
- **Resume Generation**: Creates both matching and non-matching resume examples
- **Detailed Evaluation**: Shows why each requirement passes or fails
- **PDF Export**: Download resume examples as PDFs
- **Examples Modal**: View specific evidence from resumes

## 🛠️ Setup on Replit

1. **Fork this Replit**: Click the fork button to create your own copy

2. **Set OpenAI API Key**: 
   - Go to the "Secrets" tab in your Replit
   - Add a new secret with:
     - Key: `OPENAI_API_KEY`  
     - Value: Your OpenAI API key (get one at https://openai.com/api/)

3. **Run the App**: Click the "Run" button or run `python main.py`

4. **Access the App**: Your app will be available at your Replit URL

## 💡 How to Use

1. **Enter Requirements**: 
   - Add your non-negotiable requirements (must-haves)
   - Add nice-to-have requirements (preferred)

2. **Generate Examples**: Click "Generate Candidate Examples"

3. **Review Results**: 
   - See side-by-side comparison of good vs bad resumes
   - Review AI evaluation of why each requirement passes/fails
   - Click "Show Examples" to see specific evidence

4. **Export**: Use "Export PDFs" to download the resume examples

## 🔧 Files Structure

- `main.py` - Main entry point for Replit
- `app.py` - Flask web application
- `resume_generator.py` - AI resume generation logic
- `templates/index.html` - Web interface
- `static/` - CSS, JavaScript, and assets
- `requirements.txt` - Python dependencies

## 🎯 Use Cases

- **HR Training**: Create examples for training resume screeners
- **Recruitment**: Understand what good vs bad candidates look like
- **Job Posting**: Validate that your requirements are clear
- **Screening**: Get AI assistance in evaluating actual candidates

## ⚠️ Requirements

- OpenAI API key
- Internet connection for AI analysis
- Modern web browser

## 🤖 Technology

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript  
- **AI**: OpenAI GPT models
- **PDF**: ReportLab for PDF generation
- **Deployment**: Replit ready

---

Made with ❤️ for HR professionals and recruiters