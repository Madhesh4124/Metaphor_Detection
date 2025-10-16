# 🔧 Troubleshooting Guide

Comprehensive solutions to common issues you might encounter.

---

## 🚨 Backend Issues

### Issue 1: "Module not found" errors

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**

1. **Install requirements:**
```bash
pip install -r requirements.txt
```

2. **Check Python version:**
```bash
python --version
# Should be 3.8 or higher
```

3. **Use virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

4. **Install individually:**
```bash
pip install fastapi uvicorn transformers torch numpy python-multipart pydantic
```

---

### Issue 2: Models not loading

**Error Message:**
```
ERROR: Model path not found: models/hindi_model
```

**Solutions:**

1. **Check models directory exists:**
```bash
ls models/
# Should show: hindi_model  kannada_model  tamil_model
```

2. **Check model files:**
```bash
ls models/hindi_model/
# Should show: config.json, tokenizer files, model files
```

3. **Verify file structure:**
```
models/
├── hindi_model/
│   ├── config.json
│   ├── tokenizer_config.json
│   ├── vocab.json (or tokenizer.json)
│   └── model.safetensors (or pytorch_model.bin)
├── tamil_model/
│   └── (same files)
└── kannada_model/
    └── (same files)
```

4. **Check file permissions:**
```bash
# Windows
icacls models /grant Users:F /T

# Mac/Linux
chmod -R 755 models/
```

---

### Issue 3: Port already in use

**Error Message:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solutions:**

1. **Use different port:**
```bash
uvicorn main:app --reload --port 8001
```

2. **Find and kill process (Windows):**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

3. **Find and kill process (Mac/Linux):**
```bash
lsof -ti:8000 | xargs kill -9
```

4. **Update frontend API URL:**
Edit `frontend/src/App.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

---

### Issue 4: Slow model loading

**Symptom:**
Models take 2+ minutes to load

**Solutions:**

1. **Check available RAM:**
- Models need ~2-3GB RAM
- Close other applications

2. **Use CPU instead of GPU:**
Edit `backend/main.py`:
```python
# Force CPU usage
import torch
torch.set_default_tensor_type('torch.FloatTensor')
```

3. **Load models one at a time:**
Comment out models you're not testing:
```python
languages = ['hindi']  # Only load Hindi for testing
```

---

### Issue 5: Prediction errors

**Error Message:**
```
HTTPException: Prediction failed: ...
```

**Solutions:**

1. **Check input text encoding:**
```python
# Test in Python
text = "वह आसमान छू रहा है"
print(text.encode('utf-8'))
```

2. **Verify model output:**
Add debug logging in `backend/main.py`:
```python
logger.info(f"Model output: {outputs}")
logger.info(f"Logits: {logits}")
```

3. **Check tokenizer:**
```python
# Test tokenization
inputs = tokenizer(text, return_tensors="pt")
print(inputs)
```

---

## 🌐 Frontend Issues

### Issue 6: npm install fails

**Error Message:**
```
npm ERR! code ERESOLVE
```

**Solutions:**

1. **Use legacy peer deps:**
```bash
npm install --legacy-peer-deps
```

2. **Clear cache:**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

3. **Update npm:**
```bash
npm install -g npm@latest
```

4. **Use specific Node version:**
```bash
# Install nvm (Node Version Manager)
# Then:
nvm install 18
nvm use 18
npm install
```

---

### Issue 7: Blank page in browser

**Symptom:**
Browser shows white/blank page

**Solutions:**

1. **Check browser console (F12):**
Look for error messages

2. **Common errors and fixes:**

**Error: "Failed to fetch"**
```javascript
// Check API_BASE_URL in App.jsx
const API_BASE_URL = 'http://localhost:8000';  // Correct
```

**Error: "Unexpected token"**
```bash
# Rebuild
npm run build
npm run dev
```

**Error: "Cannot read property"**
```bash
# Clear browser cache
Ctrl+Shift+Delete (Chrome)
# Or hard refresh
Ctrl+Shift+R
```

3. **Check Vite server:**
```bash
# Should show:
  VITE v5.0.8  ready in 500 ms
  ➜  Local:   http://localhost:3000/
```

---

### Issue 8: CORS errors

**Error Message:**
```
Access to fetch at 'http://localhost:8000/predict' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**

1. **Verify CORS middleware in backend:**
Check `backend/main.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Restart both servers:**
```bash
# Stop both (Ctrl+C)
# Start backend first
cd backend && uvicorn main:app --reload

# Then start frontend
cd frontend && npm run dev
```

3. **Check browser security:**
- Disable browser extensions
- Try incognito mode
- Use different browser

---

### Issue 9: Microphone not working

**Error Message:**
```
NotAllowedError: Permission denied
```

**Solutions:**

1. **Grant permissions:**
- Chrome: Click lock icon → Site settings → Microphone → Allow
- Firefox: Click shield icon → Permissions → Microphone → Allow

2. **Check HTTPS requirement:**
- Microphone API requires HTTPS or localhost
- Use `http://localhost:3000` (not IP address)

3. **Test microphone:**
```javascript
// Open browser console and run:
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => console.log('Microphone works!'))
  .catch(err => console.error('Microphone error:', err));
```

4. **Check browser compatibility:**
- Chrome/Edge: ✅ Supported
- Firefox: ✅ Supported
- Safari: ⚠️ May need additional permissions
- IE: ❌ Not supported

---

### Issue 10: Styles not loading

**Symptom:**
Page loads but looks unstyled

**Solutions:**

1. **Check CSS import:**
Verify `App.jsx` has:
```javascript
import './App.css'
```

2. **Check file paths:**
```
frontend/src/
├── App.jsx
├── App.css       ← Must exist
├── main.jsx
└── index.css     ← Must exist
```

3. **Clear Vite cache:**
```bash
rm -rf frontend/.vite
npm run dev
```

4. **Check for CSS errors:**
Open browser DevTools → Sources → Check CSS files

---

## 🔌 Connection Issues

### Issue 11: Cannot connect to backend

**Error Message:**
```
Failed to fetch
Network request failed
```

**Solutions:**

1. **Verify backend is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "System is running", ...}
```

2. **Check firewall:**
- Windows: Allow Python through firewall
- Mac: System Preferences → Security → Allow

3. **Check network:**
```bash
# Test connection
ping localhost
# Test port
telnet localhost 8000
```

4. **Use IP address:**
```javascript
// In App.jsx, try:
const API_BASE_URL = 'http://127.0.0.1:8000';
```

---

### Issue 12: Slow predictions

**Symptom:**
Predictions take >10 seconds

**Solutions:**

1. **Check CPU usage:**
- Open Task Manager (Windows) or Activity Monitor (Mac)
- Look for high CPU usage

2. **Optimize model loading:**
```python
# In main.py, add:
models[lang].eval()  # Set to evaluation mode
torch.set_grad_enabled(False)  # Disable gradients
```

3. **Process requests efficiently:**
```python
# In predict endpoint:
inputs = tokenizer(
    text,
    return_tensors="pt",
    truncation=True,
    max_length=128,  # Reduce from 512
    padding=True
)
```

4. **Check internet connection:**
- First run may download model files
- Subsequent runs should be faster

---

## 🐛 Runtime Errors

### Issue 13: "Unsupported language" error

**Error Message:**
```
Unsupported language detected. Please use Hindi, Tamil, or Kannada.
```

**Solutions:**

1. **Check input text:**
- Must be in Hindi, Tamil, or Kannada
- English and other languages not supported

2. **Verify Unicode characters:**
```python
# Test in Python
text = "वह आसमान छू रहा है"
for char in text:
    print(f"{char}: U+{ord(char):04X}")
```

3. **Check language detection logic:**
```python
# In main.py, add debug:
logger.info(f"Detecting language for: {text}")
logger.info(f"Character ranges: {[hex(ord(c)) for c in text]}")
```

---

### Issue 14: Low confidence scores

**Symptom:**
All predictions have <50% confidence

**Solutions:**

1. **Check model files:**
- Ensure models are properly fine-tuned
- Verify model.safetensors is not corrupted

2. **Test with known examples:**
```python
# Use examples from EXAMPLE_INPUTS.md
# These should have >80% confidence
```

3. **Check softmax calculation:**
```python
# In main.py, verify:
probabilities = torch.softmax(logits, dim=1)
# Should sum to 1.0
print(probabilities.sum())
```

---

### Issue 15: Translation not working

**Symptom:**
Translation shows placeholder text

**Solutions:**

1. **Expected behavior:**
- Translation is currently a placeholder
- Shows message about IndicTrans2 integration

2. **To implement real translation:**
```bash
# Install IndicTrans2
pip install indictrans2

# Update translate endpoint in main.py
# See README.md for integration guide
```

---

## 💻 System-Specific Issues

### Windows Issues

**Issue: Python not found**
```bash
# Add Python to PATH
# Or use:
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload
```

**Issue: Permission denied**
```bash
# Run as administrator
# Or:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Mac/Linux Issues

**Issue: Permission denied**
```bash
sudo chmod +x backend/main.py
# Or:
python3 -m pip install -r requirements.txt
```

**Issue: Python version conflict**
```bash
# Use python3 explicitly
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

---

## 🧪 Testing Issues

### Issue 16: test_api.py fails

**Solutions:**

1. **Ensure backend is running:**
```bash
# In one terminal:
cd backend
uvicorn main:app --reload

# In another terminal:
cd backend
python test_api.py
```

2. **Check test expectations:**
- Tests expect specific confidence levels
- May need to adjust thresholds

3. **Run individual tests:**
```python
# Edit test_api.py to run one test:
if __name__ == "__main__":
    test_health_check()
```

---

## 📱 Mobile/Responsive Issues

### Issue 17: Layout broken on mobile

**Solutions:**

1. **Check viewport meta tag:**
```html
<!-- In index.html -->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

2. **Test responsive CSS:**
```css
/* In App.css, check media queries */
@media (max-width: 768px) {
  /* Mobile styles */
}
```

3. **Use browser DevTools:**
- F12 → Toggle device toolbar
- Test different screen sizes

---

## 🆘 Emergency Fixes

### Nuclear Option 1: Complete Reinstall

```bash
# Backend
rm -rf venv __pycache__
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json .vite
npm install
```

### Nuclear Option 2: Fresh Clone

```bash
# Backup your models folder
cp -r models ../models_backup

# Delete everything else
# Re-download/clone project
# Restore models
cp -r ../models_backup models
```

---

## 📞 Getting Help

### Check Logs

**Backend logs:**
```bash
# In terminal where uvicorn is running
# Look for ERROR or WARNING messages
```

**Frontend logs:**
```javascript
// Browser console (F12)
// Look for red error messages
```

### Debug Mode

**Enable verbose logging:**
```python
# In main.py:
logging.basicConfig(level=logging.DEBUG)
```

**Check network requests:**
```
Browser DevTools → Network tab
Look for failed requests (red)
Click on request to see details
```

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Node.js 16+ installed: `node --version`
- [ ] Dependencies installed: `pip list` and `npm list`
- [ ] Models folder exists: `ls models/`
- [ ] Backend running: `curl http://localhost:8000/health`
- [ ] Frontend running: Browser shows page
- [ ] No firewall blocking: Check firewall settings
- [ ] Correct working directory: `pwd` or `cd`

---

## 🎯 Prevention Tips

1. **Always use virtual environment**
2. **Keep dependencies updated**
3. **Test after each change**
4. **Commit working code**
5. **Document custom changes**
6. **Keep backup of working version**

---

**Still stuck? Check the other documentation files or create an issue with:**
- Error message (full text)
- Steps to reproduce
- System info (OS, Python version, Node version)
- What you've already tried

---

**Good luck! 🍀**
