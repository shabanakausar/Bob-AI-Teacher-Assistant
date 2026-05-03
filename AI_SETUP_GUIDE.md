# 🤖 AI Integration Setup Guide

## Google Gemini API Setup

### Step 1: Get Your Free API Key

1. Go to **Google AI Studio**: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key (it will look like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

### Step 2: Configure the Application

1. **Create a `.env` file** in the `bob-teacher-assistant` folder:
   ```bash
   cd bob-teacher-assistant
   copy .env.example .env
   ```

2. **Edit the `.env` file** and add your API key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   (Replace with your actual API key)

### Step 3: Install Dependencies

Stop the current server (Ctrl+C) and run:

```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python312-32\python.exe -m pip install -r requirements.txt
```

### Step 4: Restart the Application

```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python312-32\python.exe app.py
```

### Step 5: Test It Out

1. Open http://localhost:5000
2. Choose MCQ Mode
3. Enter a topic (e.g., "Python Programming")
4. Click "Start Learning"
5. You should now see **real AI-generated questions** with proper options!

---

## ✨ What's New with AI Integration

### Before (Without API Key):
- ❌ Generic placeholder questions
- ❌ Same options for all questions
- ❌ No variety

### After (With API Key):
- ✅ Unique, educational questions
- ✅ Proper multiple-choice options
- ✅ Detailed explanations
- ✅ Context-aware content
- ✅ Adaptive difficulty

---

## 🔧 Troubleshooting

### "GEMINI_API_KEY not found" Warning

**Problem**: The app shows a warning about missing API key.

**Solution**: 
1. Make sure you created the `.env` file
2. Check that your API key is correct
3. Restart the application

### Questions Still Look Generic

**Problem**: Questions are still showing "Option A for [topic]"

**Solution**:
1. Verify your API key is valid
2. Check your internet connection
3. Look at the terminal for error messages
4. Make sure you installed `google-generativeai` package

### API Rate Limits

**Problem**: Getting rate limit errors

**Solution**:
- Free tier has limits (60 requests per minute)
- Wait a moment between generating questions
- Consider upgrading if you need more

---

## 📊 API Usage

### Free Tier Limits:
- **60 requests per minute**
- **1,500 requests per day**
- Perfect for personal learning!

### What Counts as a Request:
- Each question generation = 1 request
- Generating 5 MCQs = 5 requests

---

## 🎓 Best Practices

1. **Start Small**: Generate 3-5 questions at a time
2. **Be Specific**: Use clear topics (e.g., "Python loops" instead of just "Python")
3. **Save Your Work**: Export performance reports regularly
4. **Monitor Usage**: Keep track of your API calls

---

## 🔐 Security Notes

- **Never share your API key** publicly
- **Don't commit `.env` file** to version control
- The `.env` file is already in `.gitignore`
- Keep your API key secure

---

## 💡 Alternative: Running Without API Key

If you don't want to use an API key, the app will still work with:
- Sample/fallback questions
- Basic functionality
- Performance tracking

But you won't get:
- AI-generated unique questions
- Proper MCQ options
- Varied content

---

## 📞 Need Help?

If you encounter issues:
1. Check the terminal for error messages
2. Verify your API key is correct
3. Ensure internet connection is stable
4. Try regenerating your API key

---

**Ready to learn with AI? Get your API key and start now!** 🚀