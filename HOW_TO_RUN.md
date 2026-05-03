# 🚀 How to Run Bob - AI Teacher Assistant

## Quick Steps to Get Started

### 1. **Setup API Key (Optional but Recommended)**

The app can run in two modes:
- **With AI (Recommended)**: Dynamic question generation using Google Gemini AI
- **Without AI (Fallback)**: Uses sample questions

To use AI features:

1. Get a free API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the `bob-teacher-assistant` folder
3. Add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 2. **Install Dependencies**

Open terminal in the `bob-teacher-assistant` folder and run:

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask
- Flask-CORS
- google-generativeai
- python-dotenv

### 3. **Run the Application**

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### 4. **Open in Browser**

Navigate to: **http://localhost:5000**

---

## 🎯 Using the Application

1. **Choose a Learning Mode:**
   - MCQ Mode (Multiple Choice)
   - Short Answer
   - Long Answer
   - Interactive Quiz (Adaptive)

2. **Configure Your Session:**
   - Enter a topic (e.g., "Python Programming", "World History")
   - Select difficulty: EASY, MEDIUM, or HARD
   - Choose number of questions (1-20)

3. **Start Learning:**
   - Click "Start Learning"
   - Answer questions
   - Get instant feedback
   - View performance report

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the app is running.

---

## ⚠️ Troubleshooting

### Port Already in Use
If port 5000 is busy, you can change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

### Dependencies Not Installing
Try:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Python Not Found
Make sure Python 3.8+ is installed:
```bash
python --version
```

---

## 📝 Notes

- The app works without an API key but with limited functionality
- With API key: Get dynamic, AI-generated questions
- Without API key: Uses pre-defined sample questions
- All data is session-based (not saved permanently)

---

## 🎉 You're Ready!

Once the server is running and you open http://localhost:5000, you can start learning with Bob!

Happy Learning! 🚀📚