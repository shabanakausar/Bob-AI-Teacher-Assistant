# 📦 Installation Guide - Bob AI Teacher Assistant

Complete installation instructions for all platforms.

---

## 📋 Prerequisites

Before installing Bob, ensure you have:

### 1. Python Installation

**Check if Python is installed:**
```bash
python --version
```
or
```bash
python3 --version
```

**Required Version:** Python 3.8 or higher

### If Python is NOT installed:

#### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify: Open Command Prompt and type `python --version`

#### macOS:
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 🚀 Installation Steps

### Step 1: Navigate to Project Directory

**Windows (Command Prompt or PowerShell):**
```bash
cd C:\Users\DELL\Desktop\bob-teacher-assistant
```

**macOS/Linux:**
```bash
cd ~/Desktop/bob-teacher-assistant
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you get an error, try:
```bash
pip3 install -r requirements.txt
```

### Step 4: Verify Installation

```bash
pip list
```

You should see:
- Flask
- flask-cors
- Werkzeug

---

## ▶️ Running the Application

### Start the Server

**Windows:**
```bash
python app.py
```

**macOS/Linux:**
```bash
python3 app.py
```

### Expected Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Application:
Open your browser and go to:
```
http://localhost:5000
```

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 🔧 Troubleshooting

### Issue 1: "Python not found"

**Solution:**
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python39\python.exe app.py`
- Restart your terminal/command prompt

### Issue 2: "pip not found"

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue 3: "Port 5000 already in use"

**Solution:**
- Stop other applications using port 5000
- Or change port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Use different port
  ```

### Issue 4: "Module not found" errors

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue 5: Permission errors (Linux/macOS)

**Solution:**
```bash
pip install --user -r requirements.txt
```

---

## 🌐 Alternative: Run Without Installation

If you can't install Python, you can:

1. **Use Python Online IDEs:**
   - [Replit](https://replit.com)
   - [PythonAnywhere](https://www.pythonanywhere.com)
   - [Google Colab](https://colab.research.google.com)

2. **Upload the project files**
3. **Install dependencies in the online environment**
4. **Run the application**

---

## 📱 Accessing from Other Devices

To access Bob from other devices on your network:

1. Find your computer's IP address:
   - Windows: `ipconfig`
   - macOS/Linux: `ifconfig` or `ip addr`

2. Run the app with:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. Access from other devices:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

---

## 🔒 Security Notes

- The application runs in DEBUG mode by default
- For production use, set `debug=False`
- Don't expose to the internet without proper security
- Use only on trusted networks

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python 3.8+ is installed
- [ ] All dependencies are installed
- [ ] Server starts without errors
- [ ] Browser can access http://localhost:5000
- [ ] You can see the Bob interface
- [ ] You can select a learning mode
- [ ] Questions load properly

---

## 📞 Still Having Issues?

1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. Verify you're in the correct directory
4. Check if all files are present:
   - app.py
   - requirements.txt
   - templates/index.html
   - static/style.css
   - static/script.js

5. Try reinstalling dependencies:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

---

## 🎉 Success!

If you see the Bob interface in your browser, you're all set!

Start learning by:
1. Choosing a mode
2. Entering a topic
3. Clicking "Start Learning"

Happy Learning! 🚀

---

*For usage instructions, see QUICK_START.md*
*For detailed documentation, see README.md*