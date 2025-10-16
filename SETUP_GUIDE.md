# 🚀 Quick Setup Guide

This guide will help you set up and run the Multilingual Metaphor Detection application with AI-powered explanations in under 15 minutes.

## ⚡ Quick Start (10 minutes)

### Step 1: Install Backend Dependencies

Open a terminal in the project root directory and run:

```bash
pip install -r requirements.txt
```

**Wait time**: 2-3 minutes (depending on your internet speed)

### Step 2: Configure Gemini AI API Key

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

**Note**: Without this, metaphor explanations will show error messages.

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

**Wait time**: 1-2 minutes

### Step 4: Start the Backend

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload
```

**Expected output**:
```
INFO:     Gemini API configured successfully
INFO:     Loading models...
INFO:     Successfully loaded hindi model
INFO:     Successfully loaded tamil model
INFO:     Successfully loaded telugu model
INFO:     Successfully loaded kannada model
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ Backend is ready when you see "Application startup complete"

### Step 5: Start the Frontend

Open a **NEW terminal** (keep the backend running) and run:

```bash
cd frontend
npm run dev
```

**Expected output**:
```
  VITE v5.0.8  ready in 500 ms
  ➜  Local:   http://localhost:3000/
```

✅ Your browser should automatically open to http://localhost:3000

## 🎯 Testing the Application

### Test 1: Hindi Metaphor
1. Copy this text: `जिंदगी एक सफर है, मंज़िल नहीं।`
2. Paste it in the text area
3. Click "🔍 Analyze"
4. Expected result: **Metaphor** with AI explanation

### Test 2: Tamil Normal Text
1. Copy this text: `நான் பள்ளிக்கு செல்கிறேன்`
2. Paste it in the text area
3. Click "🔍 Analyze"
4. Expected result: **Normal** (green box)

### Test 3: Kannada Text
1. Copy this text: `ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ`
2. Paste it in the text area
3. Click "🔍 Analyze"
4. See the detection result

## 🔍 Verifying Everything Works

### Check Backend Health

Open your browser and go to:
```
http://localhost:8000/health
```

You should see:
```json
{
  "status": "System is running",
  "models_loaded": ["hindi", "tamil", "telugu", "kannada"]
}
```

### Check Frontend

The frontend should show:
- 🌐 Multilingual Metaphor Detector heading
- Dark glassmorphism UI design
- Text input area
- Virtual keyboard buttons (Hindi, Tamil, Telugu, Kannada)
- Speech language selector
- Three buttons: Record, Analyze, Reset
- Footer with language support info

## ❌ Common Issues & Solutions

### Issue 1: "Port 8000 already in use"

**Solution**: Kill the process or use a different port
```bash
# Use port 8001 instead
uvicorn main:app --reload --port 8001
```

Then update `frontend/src/App.jsx` line 11:
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

### Issue 2: "Module not found" errors

**Solution**: Reinstall dependencies
```bash
# For Python
pip install -r requirements.txt --force-reinstall

# For Node
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue 3: Models not loading

**Solution**: Check model files exist
```bash
# Should show 4 directories
ls models/
# Output: hindi_model  tamil_model  telugu_model  kannada_model

# Check each model has required files
ls models/hindi_model/
# Should show: config.json, tokenizer files, model files
```

### Issue 4: CORS errors in browser console

**Solution**: 
1. Ensure backend is running on port 8000
2. Check frontend is making requests to correct URL
3. Restart both backend and frontend

### Issue 5: Frontend shows blank page

**Solution**:
1. Check browser console for errors (F12)
2. Ensure Node.js version is 16 or higher: `node --version`
3. Clear browser cache and reload

## 📱 Testing on Mobile

1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` (look for inet)

2. Start frontend with host flag:
```bash
npm run dev -- --host
```

3. On your mobile device, open:
```
http://YOUR_IP_ADDRESS:3000
```

## 🎓 For Presentation

### Before Demo:
1. ✅ Start backend (wait for models to load)
2. ✅ Start frontend (verify it opens)
3. ✅ Test with one example to ensure it works
4. ✅ Prepare 3-4 example sentences
5. ✅ Have this guide open for reference

### During Demo:
1. Show the interface
2. Explain the three supported languages
3. Type/paste an example
4. Click Analyze
5. Explain the results (language, label, confidence)
6. Show translation (if metaphor)
7. Try 2-3 more examples

### Backup Plan:
- If live demo fails, have screenshots ready
- Have example outputs written down
- Explain the architecture using the README

## 📊 Performance Expectations

- **Model Loading**: 10-30 seconds (one-time at startup)
- **Language Detection**: < 1 second (using langdetect)
- **Metaphor Prediction**: 2-5 seconds
- **Translation**: 1-3 seconds (Google Translate)
- **AI Explanation**: 2-4 seconds (Google Gemini)

## 🔄 Stopping the Application

1. **Stop Frontend**: Press `Ctrl+C` in the frontend terminal
2. **Stop Backend**: Press `Ctrl+C` in the backend terminal

## 📝 Next Steps

After basic setup works:
1. ✅ Test with various inputs
2. ✅ Customize the UI colors (optional)
3. ✅ Add your name to README
4. ✅ Take screenshots for presentation
5. ✅ Practice the demo 2-3 times

## 🆘 Still Having Issues?

Check the main README.md file for:
- Detailed API documentation
- More troubleshooting tips
- Architecture explanation
- Future enhancement ideas

---

**Good luck with your project! 🎉**
