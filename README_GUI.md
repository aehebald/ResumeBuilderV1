# 🤖 Resume AI Generator - Beautiful GUI

A modern, user-friendly desktop application that transforms job descriptions into tailored resumes using AI.

## ✨ Features

- **Modern GUI Interface**: Beautiful, responsive design with dark theme
- **Job Description Input**: Large text area with file upload support
- **Side-by-Side Comparison**: View good vs. bad resume examples
- **Export Options**: Save as PDF or TXT files
- **Copy to Clipboard**: Easy copying of generated resumes
- **Progress Indication**: Real-time feedback during generation

## 🚀 Quick Start

### 1. Setup (First Time Only)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Set your OpenAI API key:

```bash
# Option 1: Environment variable
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. Run the Application

```bash
python run_gui.py
```

## 🎮 How to Use

1. **Launch the App**: Run `python run_gui.py`
2. **Input Job Description**: 
   - Paste job description in the text area, or
   - Click "📁 Browse File" to load from file
3. **Generate Resumes**: Click "✨ Generate Resumes"
4. **View Results**: Compare the good vs. bad resume examples
5. **Export**: Use Copy, Save, or Export buttons to get your resumes

## 🎨 UI Features

### Input Page
- **Clean Interface**: Modern design with professional styling
- **Smart Placeholder**: Helpful example text that disappears when you start typing
- **File Upload**: Support for .txt files
- **Progress Indicator**: Shows generation status with animated progress bar

### Results Page
- **Split View**: Side-by-side comparison of resumes
- **Color-coded**: Green for good resume, orange for bad resume
- **Action Buttons**: Copy, Save, and Export options for each resume
- **Export Options**: Generate PDFs or save as text files

## 📁 File Structure

```
JobDescriptionToPDFAIGenerator/
├── gui_app.py              # Main GUI application
├── run_gui.py              # Startup script with setup checks
├── resume_generator.py     # Core resume generation logic
├── pdf_generator.py        # PDF creation functionality
├── requirements.txt        # Python dependencies
├── .env                    # API key configuration (create this)
└── README_GUI.md          # This file
```

## 🛠️ Dependencies

- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `reportlab>=4.0.0` - PDF generation
- `ttkbootstrap>=1.10.1` - Modern tkinter styling
- `pillow>=10.0.0` - Image processing support

## 🎯 Tips for Best Results

1. **Detailed Job Descriptions**: Include requirements, responsibilities, and company info
2. **Industry Context**: The AI automatically detects industry and tailors accordingly
3. **Export Options**: Use PDF for professional applications, TXT for further editing

## 🐛 Troubleshooting

### "OpenAI API key not configured"
- Set your API key as environment variable or in .env file
- Make sure your API key has sufficient credits

### "Missing dependencies" 
- Run: `pip install -r requirements.txt`
- Make sure virtual environment is activated

### GUI doesn't start
- Check Python version (3.8+ required)
- Try: `python3 run_gui.py` instead of `python run_gui.py`

## 🔮 What Makes This Special

- **AI-Powered**: Uses OpenAI's GPT models for intelligent resume generation
- **Industry-Aware**: Automatically adapts to different industries (tech, marketing, finance, etc.)
- **Comparison Learning**: Shows both good and bad examples for learning
- **Professional Quality**: Generates properly formatted, ATS-friendly resumes
- **User-Friendly**: No command-line knowledge required

---

Enjoy creating perfectly tailored resumes! 🎉