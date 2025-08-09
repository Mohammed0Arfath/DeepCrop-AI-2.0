# 🚀 EXACTLY WHERE TO RUN THE COMMANDS

## Step 1: Open Command Prompt/Terminal

### Windows:
1. Press `Windows + R` 
2. Type `cmd`
3. Press Enter
4. You'll see a black window with something like: `C:\Users\YourName>`

### Mac:
1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter
4. You'll see a window with something like: `YourName@MacBook ~ %`

### Linux:
1. Press `Ctrl + Alt + T`
2. You'll see a terminal window

## Step 2: Navigate to Your Project Folder

Type this command and press Enter:
```bash
cd path/to/sugarcane-disease-detection
```

**Replace "path/to" with the actual location!** For example:
- If it's on Desktop: `cd Desktop/sugarcane-disease-detection`
- If it's in Downloads: `cd Downloads/sugarcane-disease-detection`
- Windows full path: `cd C:\Users\YourName\Desktop\sugarcane-disease-detection`

## Step 3: Configure Environment (Run ONCE)

**In the same Command Prompt/Terminal window**, type these commands one by one:

```bash
cp .env.example .env
```
*Press Enter after typing this*

**Note for Windows users**: If `cp` doesn't work, use:
```bash
copy .env.example .env
```

## Step 4: Set Up Backend

**Still in the same Command Prompt/Terminal window**, type these commands one by one:

```bash
cd backend
```
*Press Enter*

```bash
python -m venv venv
```
*Press Enter (this creates a virtual environment)*

```bash
# For Windows:
venv\Scripts\activate

# For Mac/Linux:
source venv/bin/activate
```
*Press Enter (this activates the virtual environment)*

```bash
pip install -r requirements.txt
```
*Press Enter (this installs all required packages - takes a few minutes)*

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*Press Enter (this starts the backend server)*

**✅ SUCCESS**: You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**🚨 IMPORTANT**: Keep this window open! Don't close it.

## Step 5: Set Up Frontend (Open NEW Window)

**Open a SECOND Command Prompt/Terminal window** (don't close the first one):

### Windows:
1. Press `Windows + R` again
2. Type `cmd` again
3. Press Enter

### Mac/Linux:
1. Open a new Terminal window (Cmd+T on Mac, or Ctrl+Shift+T on Linux)

**In this NEW window**, type these commands:

```bash
cd path/to/sugarcane-disease-detection
```
*Replace with your actual path, same as before*

```bash
cd frontend
```
*Press Enter*

```bash
npm install
```
*Press Enter (this installs frontend packages - takes a few minutes)*

```bash
npm run dev
```
*Press Enter (this starts the website)*

**✅ SUCCESS**: You should see:
```
  Local:   http://localhost:5173/
```

## Step 6: Open Your Browser

1. Open any web browser (Chrome, Firefox, Safari, Edge)
2. Go to: `http://localhost:5173`
3. You should see the Sugarcane Disease Detection website!

## 📋 Summary - You Should Have:

1. **First Command Prompt/Terminal**: Running the backend (showing Uvicorn messages)
2. **Second Command Prompt/Terminal**: Running the frontend (showing Vite messages)
3. **Web Browser**: Open to http://localhost:5173 showing your website

## 🛑 To Stop Everything:

1. In the first window (backend): Press `Ctrl + C`
2. In the second window (frontend): Press `Ctrl + C`
3. Close both Command Prompt/Terminal windows

## ❌ If Something Goes Wrong:

### "python is not recognized"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### "npm is not recognized"  
- Install Node.js from https://nodejs.org/
- Restart your computer after installation

### "No such file or directory"
- Make sure you're in the right folder
- Use `dir` (Windows) or `ls` (Mac/Linux) to see what files are in your current folder
- You should see folders like "backend", "frontend", "examples"

### Port already in use
- Close other applications that might be using the same ports
- Or change the port numbers in the commands

## 🎯 Quick Visual Guide:

```
Window 1 (Backend):
C:\path\to\sugarcane-disease-detection\backend> uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
INFO: Uvicorn running on http://0.0.0.0:8000 ← KEEP THIS RUNNING

Window 2 (Frontend):  
C:\path\to\sugarcane-disease-detection\frontend> npm run dev
Local: http://localhost:5173/ ← KEEP THIS RUNNING TOO

Browser:
http://localhost:5173 ← YOUR WEBSITE IS HERE!
```

**Remember**: Both windows must stay open for the system to work!
