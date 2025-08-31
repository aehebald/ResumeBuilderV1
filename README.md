# Resume Generator

A Python application that uses the ChatGPT API to generate two types of resumes based on job descriptions:
1. **Matching Resume**: A resume for a candidate who fits all the job requirements
2. **Non-Matching Resume**: A resume for a candidate who doesn't fit the job requirements

## Setup

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Generate PDF resumes (default):
```bash
source .venv/bin/activate
python main.py --job-file sample_job_description.txt
```

### Generate text resumes:
```bash
source .venv/bin/activate
python main.py --job-file sample_job_description.txt --format txt
```

### Using job description text directly:
```bash
source .venv/bin/activate
python main.py --job-text "Software Engineer position requiring Python, Django, and 5+ years experience..."
```

### Custom output directory:
```bash
source .venv/bin/activate
python main.py --job-file sample_job_description.txt --output-dir my_resumes
```

## Output

By default, the application generates two PDF files:
- `matching_resume.pdf` - Resume of a qualified candidate
- `non_matching_resume.pdf` - Resume of an unqualified candidate

Use `--format txt` to generate text files instead.

## How it Works

1. **Job Analysis**: Parses the job description to extract:
   - Must-have requirements
   - Nice-to-have requirements  
   - Job title and industry
   - Key responsibilities

2. **Resume Generation**: Creates two distinct resumes:
   - **Matching**: Candidate with all must-haves and most nice-to-haves
   - **Non-Matching**: Candidate lacking the required qualifications

## Example

Try the included sample to generate PDF resumes:
```bash
source .venv/bin/activate
python main.py --job-file sample_job_description.txt
```

Or test the formatting without API calls:
```bash
source .venv/bin/activate
python test_resume_format.py
```

This will analyze the Senior Software Engineer position and generate appropriate matching/non-matching resumes in PDF format.