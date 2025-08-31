# 🧪 API Testing Instructions

## Setup (One-time)

1. **Set up your OpenAI API key:**
```bash
source .venv/bin/activate
python setup_api_key.py
```

2. **Or manually create .env file:**
```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

## Run API Tests

```bash
source .venv/bin/activate
python test_api.py
```

## What the Test Does

### 📋 **3 Job Types Tested:**

1. **Tech Job (JavaScript/React)**
   - Must-haves: 5+ years JS, React/Node.js, SQL, APIs, Git, CS degree
   - Nice-to-haves: AWS, Docker, TypeScript, GraphQL, CI/CD

2. **Marketing Job (Digital Marketing)**  
   - Must-haves: 4+ years marketing, Google/Facebook Ads, Analytics, CMS
   - Nice-to-haves: HubSpot, Salesforce, Video editing, SEO/SEM

3. **Data Science Job (Python/ML)**
   - Must-haves: PhD/Master's, 3+ years Python, ML algorithms, Statistics
   - Nice-to-haves: Deep Learning, Big Data, Cloud, R, MLOps

### 🔍 **What Gets Tested:**

- ✅ Job requirement parsing (must-haves vs nice-to-haves)
- ✅ Resume generation for matching candidates
- ✅ Resume generation for non-matching candidates  
- ✅ PDF creation and formatting
- ✅ Requirement extraction accuracy

### 📄 **Expected Output:**

```
api_test_output/
├── tech_job/
│   ├── matching_resume.pdf
│   └── non_matching_resume.pdf
├── marketing_job/
│   ├── matching_resume.pdf
│   └── non_matching_resume.pdf
├── data_science/
│   ├── matching_resume.pdf
│   └── non_matching_resume.pdf
└── job_analyses.json
```

## Sample Test Output

```
🚀 TESTING CHATGPT API WITH DIFFERENT JOB REQUIREMENTS
======================================================================

📋 TEST 1: TECH JOB (JavaScript/React)
--------------------------------------------------
Testing job requirements parsing...
✅ Job analysis completed!
   Must-haves found: 6
   Nice-to-haves found: 7
   Job title: Senior Full-Stack Developer

🔍 PARSED REQUIREMENTS:
Must-haves: ['5+ years of JavaScript development', 'React.js and Node.js skills', 'SQL database experience'] ...
Nice-to-haves: ['AWS cloud platform', 'Docker containerization', 'TypeScript experience'] ...

📝 Generating resumes...
✅ Tech job PDFs generated:
   📄 Matching: api_test_output/tech_job/matching_resume.pdf
   📄 Non-matching: api_test_output/tech_job/non_matching_resume.pdf
```

## Cost Estimate

- **Parsing**: ~$0.01 per job description
- **Resume generation**: ~$0.05 per resume 
- **Total per test run**: ~$0.30 (6 resumes + 3 job analyses)

This is a comprehensive test that validates both the requirement parsing and resume generation with real ChatGPT API calls!