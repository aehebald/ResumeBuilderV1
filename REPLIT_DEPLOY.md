# 🚀 Replit Deployment Guide

## Quick Deploy Steps

1. **Create Replit Account**: Go to https://replit.com and sign up

2. **Import Project**: 
   - Click "Create Repl"
   - Choose "Import from GitHub"
   - Or upload these files directly

3. **Configure Environment**:
   - Click on "Secrets" tab (🔒 icon)
   - Add secret:
     - Key: `OPENAI_API_KEY`
     - Value: `your-actual-openai-api-key`

4. **Install Dependencies** (automatic on first run):
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Application**:
   - Click the green "Run" button
   - Or run: `python main.py`

6. **Access Your App**:
   - Your app will be available at the URL shown in Replit
   - Format: `https://your-repl-name.your-username.repl.co`

## 🔑 Getting OpenAI API Key

1. Go to https://openai.com/api/
2. Sign up / Log in
3. Go to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-...`)
6. Add it to Replit Secrets

## ✅ What's Included

All files are ready for Replit deployment:
- ✅ `main.py` - Entry point for Replit
- ✅ `requirements.txt` - Dependencies
- ✅ `.replit` - Replit configuration
- ✅ `replit.nix` - System packages
- ✅ Flask app with all features
- ✅ Static files (CSS, JS)
- ✅ Templates

## 🛠️ Troubleshooting

**App won't start?**
- Check that OPENAI_API_KEY is set in Secrets
- Check the console for error messages
- Make sure all files uploaded correctly

**Dependencies not installing?**
- Replit should auto-install from requirements.txt
- If not, run `pip install -r requirements.txt` in Shell

**Port issues?**
- App runs on port 5001
- Replit should handle port forwarding automatically

## 📱 Features Available

Once deployed, your app includes:
- Web-based resume analysis interface
- AI-powered requirement evaluation
- PDF export functionality
- Real-time resume screening
- Professional UI for HR teams

## 🔄 Updates

To update your deployed app:
1. Make changes to your files
2. Replit auto-saves and restarts
3. Refresh your browser to see changes

---

🎉 **You're ready to deploy!** Click "Run" and start screening resumes with AI!