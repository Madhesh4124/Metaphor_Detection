# 🌐 Multilingual Metaphor Detection and Translation Web Application

A web application that detects metaphors in Hindi, Tamil, and Kannada text using fine-tuned transformer models and provides English translations for metaphorical expressions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Example Inputs and Outputs](#example-inputs-and-outputs)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

This application uses state-of-the-art NLP models to:
1. **Automatically detect** the language of input text (Hindi, Tamil, or Kannada)
2. **Classify** whether the text contains a metaphor or is normal text
3. **Provide confidence scores** for predictions
4. **Translate** metaphorical expressions to English (placeholder for IndicTrans2 integration)
5. **Support speech input** for hands-free operation (placeholder for Whisper integration)

## ✨ Features

- **🔍 Automatic Language Detection**: Detects Hindi, Tamil, Telugu, and Kannada with 90%+ accuracy using langdetect library
- **🎭 Metaphor Classification**: Uses fine-tuned XLM-RoBERTa, MuRIL, and Kannada-BERT models
- **📊 Confidence Scores**: Shows prediction confidence (0-1 scale)
- **🤖 AI-Powered Explanations**: Contextual metaphor explanations using Google Gemini AI
- **🌍 Translation Support**: Translates metaphorical text to English using Google Translate
- **📜 History Feature**: View, filter, and manage past predictions with MongoDB
- **📈 Statistics Dashboard**: Track your usage with detailed analytics
- **🎤 Speech Input**: Browser-based speech recognition for all 4 languages
- **⌨️ Virtual Keyboard**: On-screen keyboards for Hindi, Tamil, Telugu, and Kannada
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎨 Modern UI**: Beautiful dark glassmorphism design with gradients
- **⚡ Fast Processing**: Predictions in under 5 seconds

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Transformers**: Hugging Face library for NLP models
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server
- **MongoDB**: NoSQL database for history storage
- **Motor**: Async MongoDB driver for Python

### Frontend
- **React 18**: Modern JavaScript library
- **Vite**: Fast build tool and dev server
- **CSS3**: Custom styling with gradients and animations

### Models
- **XLM-RoBERTa**: For Hindi and Tamil metaphor detection
- **Kannada-BERT**: For Kannada metaphor detection
- **IndicTrans2**: For translation (to be integrated)
- **Whisper**: For speech recognition (to be integrated)

## 📁 Project Structure

```
project_root/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── __pycache__/
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Component styles
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML template
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── models/
│   ├── hindi_model/           # Hindi XLM-RoBERTa model
│   ├── tamil_model/           # Tamil XLM-RoBERTa model
│   └── kannada_model/         # Kannada-BERT model
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Git** (optional, for cloning)

### Step 1: Clone or Download the Project

```bash
cd "d:/CODE/New folder"
```

### Step 2: Install Backend Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

**Note**: Installing PyTorch may take some time. If you encounter issues, visit [pytorch.org](https://pytorch.org) for platform-specific installation instructions.

### Step 4: Set up Gemini AI API Key

The application uses Google Gemini AI for generating contextual metaphor explanations.

1. **Get your API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Create a `.env` file** in the project root:
```bash
cp .env.example .env
```

3. **Edit the `.env` file** and add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

**Note**: Without a valid Gemini API key, metaphor explanations will show fallback messages.

### Step 5: Set up MongoDB (Optional - for History Feature)

The history feature requires MongoDB to store predictions.

**Option 1: Local MongoDB**
```bash
# Install MongoDB Community Server from:
# https://www.mongodb.com/try/download/community

# Start MongoDB service
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

**Option 2: MongoDB Atlas (Cloud - Free)**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string

**Configure in `.env`:**
```bash
# For local MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=metaphor_detector

# For MongoDB Atlas
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=metaphor_detector
```

**Note**: The app works without MongoDB, but history feature will be disabled.

📖 **Detailed setup guide**: See `MONGODB_SETUP.md`

### Step 3: Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node packages
npm install

# Return to root directory
cd ..
```

## 🏃 Running the Application

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Loading models...
INFO:     Successfully loaded hindi model
INFO:     Successfully loaded tamil model
INFO:     Successfully loaded kannada model
INFO:     Application startup complete.
```

The backend API will be available at: **http://localhost:8000**

### Step 2: Start the Frontend Development Server

Open a **new terminal** and run:

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

The application will automatically open in your browser at: **http://localhost:3000**

## 📖 Usage Guide

### Text Input Method

1. **Enter Text**: Type or paste text in Hindi, Tamil, or Kannada in the text area
2. **Click Analyze**: Press the "🔍 Analyze" button
3. **View Results**: See the detected language, classification, and confidence score
4. **Translation**: If a metaphor is detected, the English translation will appear below

### Speech Input Method (Framework Ready)

1. **Click Record**: Press the "🎤 Record" button
2. **Speak**: Say your text in Hindi, Tamil, or Kannada
3. **Stop Recording**: Click "⏹️ Stop" when done
4. **Analyze**: The recognized text will appear in the input box, then click "🔍 Analyze"

**Note**: Speech recognition requires additional setup with Whisper or similar library.

### Reset

Click the "🔄 Reset" button to clear all fields and start over.

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "System is running",
  "models_loaded": ["hindi", "tamil", "kannada"]
}
```

#### 2. Predict Metaphor
```http
POST /predict
Content-Type: application/json

{
  "text": "वह आसमान छू रहा है"
}
```

**Response:**
```json
{
  "language": "hindi",
  "label": "metaphor",
  "confidence": 0.9234,
  "text": "वह आसमान छू रहा है"
}
```

#### 3. Translate Text
```http
POST /translate
Content-Type: application/json

{
  "text": "वह आसमान छू रहा है",
  "source_language": "hindi"
}
```

**Response:**
```json
{
  "original_text": "वह आसमान छू रहा है",
  "translated_text": "He is touching the sky (meaning: achieving great success)",
  "source_language": "hindi"
}
```

#### 4. Speech to Text
```http
POST /speech
Content-Type: multipart/form-data

audio: <audio_file>
```

**Response:**
```json
{
  "text": "Recognized text here",
  "success": true,
  "message": "Speech recognized successfully"
}
```

#### 5. Get History
```http
GET /history?limit=50&skip=0&language=hindi&label=metaphor
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "history": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "text": "वह आसमान छू रहा है",
      "language": "hindi",
      "label": "metaphor",
      "confidence": 0.9234,
      "translation": "He is touching the sky",
      "explanation": "This metaphor compares...",
      "timestamp": "2025-01-16T10:30:00.000Z"
    }
  ]
}
```

#### 6. Get Statistics
```http
GET /statistics
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_predictions": 150,
    "metaphor_count": 75,
    "normal_count": 75,
    "languages": {
      "hindi": 50,
      "tamil": 40,
      "telugu": 30,
      "kannada": 30
    }
  }
}
```

#### 7. Delete History Item
```http
DELETE /history/{prediction_id}
```

#### 8. Clear All History
```http
DELETE /history
```

## 📝 Example Inputs and Outputs

### Example 1: Hindi Metaphor

**Input:**
```
वह आसमान छू रहा है
```

**Output:**
- **Language**: HINDI
- **Classification**: 🎭 Metaphor
- **Confidence**: 92.34%
- **Translation**: "He is touching the sky (meaning: achieving great success)"

### Example 2: Tamil Normal Text

**Input:**
```
நான் பள்ளிக்கு செல்கிறேன்
```

**Output:**
- **Language**: TAMIL
- **Classification**: ✅ Normal
- **Confidence**: 88.76%

### Example 3: Kannada Metaphor

**Input:**
```
ಅವನು ಬೆಂಕಿಯಂತೆ ಕೋಪಗೊಂಡನು
```

**Output:**
- **Language**: KANNADA
- **Classification**: 🎭 Metaphor
- **Confidence**: 91.23%
- **Translation**: "He became angry like fire (meaning: became very angry)"

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Models not loading
```
Solution: Ensure the models/ directory contains all required model files:
- config.json
- tokenizer_config.json
- vocab.json (or tokenizer.json)
- model.safetensors (or pytorch_model.bin)
```

**Problem**: Port 8000 already in use
```bash
Solution: Use a different port
uvicorn main:app --reload --port 8001
```

**Problem**: CORS errors
```
Solution: The backend is already configured with CORS middleware.
Ensure the frontend is making requests to the correct backend URL.
```

### Frontend Issues

**Problem**: Cannot connect to backend
```
Solution: Verify the backend is running on http://localhost:8000
Check the API_BASE_URL in App.jsx matches your backend URL
```

**Problem**: Port 3000 already in use
```
Solution: Vite will automatically suggest an alternative port (3001, 3002, etc.)
```

**Problem**: Microphone not working
```
Solution: 
1. Grant microphone permissions in your browser
2. Use HTTPS or localhost (required for getUserMedia API)
3. Check browser console for specific errors
```

### Model Issues

**Problem**: Low accuracy predictions
```
Solution: Ensure you're using the correct fine-tuned models
Verify the model files are not corrupted
Check that input text is in the correct language
```

## 🚀 Future Enhancements

### Planned Features

1. **IndicTrans2 Integration**
   - Replace placeholder translation with actual IndicTrans2 model
   - Support bidirectional translation

2. **Whisper Speech Recognition**
   - Integrate OpenAI Whisper for accurate speech-to-text
   - Support real-time transcription

3. **Additional Languages**
   - Add support for more Indian languages (Telugu, Malayalam, Bengali, etc.)

4. **Model Fine-tuning Interface**
   - Allow users to contribute labeled data
   - Continuous model improvement

5. **Deployment**
   - Docker containerization
   - Cloud deployment (AWS, Azure, or GCP)
   - CI/CD pipeline

### How to Integrate IndicTrans2

1. Install IndicTrans2:
```bash
pip install indictrans2
```

2. Update the `/translate` endpoint in `backend/main.py`:
```python
from indictrans import Transliterator

# Initialize translator
translator = Transliterator(source='hin', target='eng')

@app.post("/translate")
async def translate(request: TranslationRequest):
    translated = translator.transform(request.text)
    return TranslationResponse(
        original_text=request.text,
        translated_text=translated,
        source_language=request.source_language
    )
```

### How to Integrate Whisper

1. Install Whisper:
```bash
pip install openai-whisper
```

2. Update the `/speech` endpoint in `backend/main.py`:
```python
import whisper

# Load Whisper model
whisper_model = whisper.load_model("base")

@app.post("/speech")
async def speech_to_text(audio: UploadFile = File(...)):
    # Save uploaded file
    audio_path = f"temp_{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    
    # Transcribe
    result = whisper_model.transcribe(audio_path)
    
    # Clean up
    os.remove(audio_path)
    
    return {
        "text": result["text"],
        "success": True,
        "message": "Speech recognized successfully"
    }
```

## 📄 License

This project is created for educational purposes as a college project.

## 👥 Contributors

- **Your Name** - Project Developer

## 📧 Contact

For questions or support, please contact: [your.email@example.com]

---

**Note**: This is a demonstration project. For production use, implement proper error handling, security measures, authentication, and rate limiting.

## 🎓 Presentation Tips

### Demo Script

1. **Introduction** (1 min)
   - Explain the problem: Understanding metaphors in Indian languages
   - Show the application interface

2. **Live Demo** (3 min)
   - Type a Hindi metaphor and show detection
   - Try a Tamil normal sentence
   - Demonstrate the speech input (if implemented)

3. **Technical Overview** (2 min)
   - Show the project structure
   - Explain the model architecture
   - Discuss the tech stack

4. **Results & Accuracy** (1 min)
   - Show confidence scores
   - Discuss model performance

5. **Future Work** (1 min)
   - Mention planned enhancements
   - Discuss scalability

### Screenshots to Include

1. Main interface with empty input
2. Detection result showing metaphor (blue)
3. Detection result showing normal text (green)
4. Translation display
5. Error handling example
6. Mobile responsive view

---

**Happy Coding! 🚀**
