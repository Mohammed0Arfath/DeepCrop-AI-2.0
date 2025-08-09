# 🌾 Complete Beginner's Guide to Running Sugarcane Disease Detection System

This guide will help you run the sugarcane disease detection system step by step, even if you're completely new to programming.

## 📋 What You Need to Install First

### Step 1: Install Python (for Backend)
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. **IMPORTANT**: During installation, check the box "Add Python to PATH"
4. Click "Install Now"
5. Test installation: Open Command Prompt (Windows) or Terminal (Mac/Linux) and type:
   ```
   python --version
   ```
   You should see something like "Python 3.11.x"

### Step 2: Install Node.js (for Frontend)
1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Install with default settings
4. Test installation: In Command Prompt/Terminal, type:
   ```
   node --version
   npm --version
   ```
   You should see version numbers for both

## 🚀 Running the System

### Step 3: Open Command Prompt/Terminal
- **Windows**: Press `Windows + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 4: Navigate to Your Project
```bash
# Replace this path with where you saved the project
cd path/to/sugarcane-disease-detection

# For example, if it's on your Desktop:
# Windows: cd C:\Users\YourName\Desktop\sugarcane-disease-detection
# Mac/Linux: cd ~/Desktop/sugarcane-disease-detection
```

### Step 5: Set Up the Backend (Python Server)

#### 5a. Navigate to Backend Folder
```bash
cd backend
```

#### 5b. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

#### 5c. Install Required Packages
```bash
pip install -r requirements.txt
```
*This might take a few minutes to download and install all packages*

#### 5d. Start the Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Success Signs:**
- You should see messages like "Uvicorn running on http://0.0.0.0:8000"
- No error messages
- **Keep this window open!** The backend is now running.

### Step 6: Set Up the Frontend (React Website)

#### 6a. Open a NEW Command Prompt/Terminal Window
*Don't close the backend window - open a new one*

#### 6b. Navigate to Frontend Folder
```bash
# Go back to main project folder first
cd path/to/sugarcane-disease-detection
cd frontend
```

#### 6c. Install Frontend Packages
```bash
npm install
```
*This might take a few minutes*

#### 6d. Start the Frontend Server
```bash
npm run dev
```

**✅ Success Signs:**
- You should see "Local: http://localhost:5173"
- No error messages
- **Keep this window open too!**

## 🎉 Access Your Application

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: **http://localhost:5173**
3. You should see the Sugarcane Disease Detection website!

## 🧪 Testing the System

1. **Select Disease Type**: Choose "Dead Heart" or "Tiller"
2. **Upload Image**: Click to upload any image (for testing)
3. **Fill Questionnaire**: Answer the 15 yes/no questions
4. **Click "Analyze Disease"**: See the results!

## ❌ Common Problems and Solutions

### Problem: "python is not recognized"
**Solution**: Python wasn't added to PATH during installation
- Reinstall Python and check "Add Python to PATH"
- Or search "Environment Variables" in Windows and add Python to PATH

### Problem: "npm is not recognized"
**Solution**: Node.js wasn't installed properly
- Reinstall Node.js from nodejs.org
- Restart your computer after installation

### Problem: "Port already in use"
**Solution**: Something is already using the port
- Close other applications
- Or change the port number:
  ```bash
  # For backend, use different port:
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
  
  # For frontend, it will automatically suggest a different port
  ```

### Problem: Backend shows "Model not found" warnings
**Solution**: This is normal! The system works with mock data for testing
- To use real models, add your .pt and .joblib files to the `models/` folder

### Problem: Can't access http://localhost:5173
**Solution**: 
- Make sure both backend and frontend are running
- Check if your firewall is blocking the ports
- Try http://127.0.0.1:5173 instead

## 🛑 How to Stop the System

1. **Stop Frontend**: In the frontend terminal, press `Ctrl + C`
2. **Stop Backend**: In the backend terminal, press `Ctrl + C`
3. **Deactivate Virtual Environment** (if you used one):
   ```bash
   deactivate
   ```

## 📁 Project Structure (What Each Folder Does)

```
sugarcane-disease-detection/
├── backend/           # Python server (AI processing)
├── frontend/          # React website (user interface)
├── models/            # Your AI model files go here
├── examples/          # Sample data for testing
└── README.md          # Detailed documentation
```

## 🆘 Need More Help?

1. **Check the main README.md** for detailed technical information
2. **Look at the examples/ folder** for sample data
3. **Make sure both terminal windows stay open** while using the system
4. **Try refreshing your browser** if the website doesn't load

## 🎯 Quick Start Checklist

- [ ] Install Python 3.11+
- [ ] Install Node.js (LTS version)
- [ ] Open terminal/command prompt
- [ ] Navigate to project folder
- [ ] Set up backend (`cd backend`, create venv, install packages, run server)
- [ ] Open NEW terminal window
- [ ] Set up frontend (`cd frontend`, install packages, run server)
- [ ] Open browser to http://localhost:5173
- [ ] Test with sample data

**Remember**: Keep both terminal windows open while using the system!
