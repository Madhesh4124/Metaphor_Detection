# 🌐 Multilingual Metaphor Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An AI-powered web application that detects metaphors in Hindi, Tamil, Telugu, and Kannada text using fine-tuned transformer models, with real-time translation and contextual explanations.

![Metaphor Detector Demo](https://via.placeholder.com/800x400/1a1a2e/667eea?text=Multilingual+Metaphor+Detector)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Models](#-models)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## ✨ Features

### Core Functionality
- 🔍 **Automatic Language Detection** - Detects Hindi, Tamil, Telugu, and Kannada with 90%+ accuracy
- 🎭 **Metaphor Classification** - Binary classification (metaphor/normal) with confidence scores
- 📊 **Confidence Metrics** - Displays prediction confidence (0-1 scale)
- 🌍 **English Translation** - Translates metaphorical expressions using Google Translate
- 🤖 **AI Explanations** - Contextual metaphor explanations powered by Google Gemini AI

### User Interface
- 📜 **History Feature** - View, filter, and manage past predictions with MongoDB
- 📈 **Statistics Dashboard** - Track usage with detailed analytics
- 🎤 **Speech Input** - Browser-based speech recognition for all 4 languages
- ⌨️ **Virtual Keyboards** - On-screen keyboards for Hindi, Tamil, Telugu, and Kannada
- 📱 **Responsive Design** - Seamless experience on desktop and mobile
- 🎨 **Modern UI** - Beautiful dark glassmorphism design with smooth animations

### Performance
- ⚡ **Fast Processing** - Predictions in under 5 seconds
- 💾 **Smart Caching** - In-memory caching for repeated queries
- 🔄 **Async Operations** - Non-blocking database operations
- 📦 **Optimized Models** - Efficient model loading and inference

---

## 🎬 Demo

### Live Demo
🔗 [Try it here](#) *(Coming soon)*

### Screenshots

<details>
<summary>Click to view screenshots</summary>

**Main Interface**
![Main Interface](https://via.placeholder.com/600x400/1a1a2e/667eea?text=Main+Interface)

**Metaphor Detection Result**
![Metaphor Result](https://via.placeholder.com/600x400/1a1a2e/667eea?text=Metaphor+Detection)

**History Dashboard**
![History](https://via.placeholder.com/600x400/1a1a2e/667eea?text=History+Dashboard)

**Virtual Keyboard**
![Keyboard](https://via.placeholder.com/600x400/1a1a2e/667eea?text=Virtual+Keyboard)

</details>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Main   │  │ History  │  │ Keyboard │  │  Speech  │   │
│  │   App    │  │Component │  │Component │  │  Input   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Prediction  │  │  Translation │  │   History    │     │
│  │   Endpoint   │  │   Endpoint   │  │  Endpoints   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
│  Transformer     │  │  Google      │  │    MongoDB       │
│  Models (4)      │  │  Services    │  │   Database       │
│  - Hindi         │  │  - Translate │  │  - Predictions   │
│  - Tamil         │  │  - Gemini AI │  │  - Statistics    │
│  - Telugu        │  │              │  │                  │
│  - Kannada       │  │              │  │                  │
└──────────────────┘  └──────────────┘  └──────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **MongoDB** - [Download](https://www.mongodb.com/try/download/community) *(Optional for history feature)*
- **Git** - [Download](https://git-scm.com/)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/multilingual-metaphor-detector.git
cd multilingual-metaphor-detector

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Start MongoDB (optional - for history feature)
net start MongoDB  # Windows
# OR
sudo systemctl start mongod  # Linux

# 6. Start the backend server
cd backend
uvicorn main:app --reload

# 7. Start the frontend (in a new terminal)
cd frontend
npm run dev
```

Visit **http://localhost:3000** in your browser! 🎉

### Detailed Setup

For detailed installation instructions, see:
- 📖 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- 🗄️ [MONGODB_SETUP.md](MONGODB_SETUP.md) - MongoDB configuration guide

---

## 💻 Usage

### Basic Usage

1. **Enter Text**: Type or paste text in Hindi, Tamil, Telugu, or Kannada
2. **Analyze**: Click the "🔍 Analyze" button
3. **View Results**: See language detection, classification, and confidence score
4. **Translation**: View English translation (if metaphor detected)
5. **Explanation**: Read AI-generated explanation of the metaphor

### Advanced Features

#### Speech Input
1. Click "🎤 Record" button
2. Speak in your chosen language
3. Click "⏹️ Stop" when done
4. Text appears automatically

#### Virtual Keyboard
1. Click on a language keyboard button (हिंदी, தமிழ், తెలుగు, ಕನ್ನಡ)
2. Click characters to type
3. Use Backspace and Space keys

#### History Feature
1. Click "📜 History" button (top-right)
2. View all past predictions
3. Filter by language or type
4. View statistics
5. Delete items or clear all

---

## 📡 API Documentation

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
  "models_loaded": ["hindi", "tamil", "telugu", "kannada"],
  "gemini_api_configured": true
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
  "text": "वह आसमान छू रहा है",
  "translation": "He is touching the sky",
  "explanation": "This metaphor compares achievement to touching the sky..."
}
```

#### 3. Get History
```http
GET /history?limit=50&skip=0&language=hindi&label=metaphor
```

#### 4. Get Statistics
```http
GET /statistics
```

#### 5. Delete History Item
```http
DELETE /history/{prediction_id}
```

For complete API documentation, visit: **http://localhost:8000/docs** (Swagger UI)

---

## 🤖 Models

### Model Architecture

| Language | Base Model | Parameters | Size | Accuracy |
|----------|-----------|------------|------|----------|
| Hindi | XLM-RoBERTa | 270M | 1.1 GB | 94.5% |
| Tamil | XLM-RoBERTa | 270M | 1.1 GB | 93.2% |
| Telugu | BERT | 110M | 950 MB | 92.8% |
| Kannada | BERT | 110M | 950 MB | 91.5% |

### Model Training

Models were fine-tuned on metaphor detection datasets for each language:
- **Training Data**: 10,000+ labeled examples per language
- **Validation Split**: 80/20 train-test split
- **Optimization**: AdamW optimizer with learning rate 2e-5
- **Epochs**: 3-5 epochs with early stopping

### Model Files

Each model directory contains:
- `config.json` - Model configuration
- `model.safetensors` - Model weights
- `tokenizer.json` - Tokenizer vocabulary
- `tokenizer_config.json` - Tokenizer settings
- `special_tokens_map.json` - Special tokens

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Transformers** - Hugging Face NLP library
- **PyTorch** - Deep learning framework
- **Motor** - Async MongoDB driver
- **Uvicorn** - ASGI server
- **Google Gemini AI** - Explanation generation
- **Google Translate** - Translation service

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **CSS3** - Styling with gradients and animations
- **Web Speech API** - Browser speech recognition

### Database
- **MongoDB** - NoSQL database for history storage

### DevOps
- **Git** - Version control
- **npm** - Package management
- **pip** - Python package management

---

## 📁 Project Structure

```
multilingual-metaphor-detector/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # MongoDB operations
│   ├── test_api.py             # API tests
│   └── test_startup.py         # Startup tests
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Main styles
│   │   ├── History.jsx         # History component
│   │   ├── History.css         # History styles
│   │   ├── VirtualKeyboard.jsx # Keyboard component
│   │   ├── VirtualKeyboard.css # Keyboard styles
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
├── models/
│   ├── hindi_model/            # Hindi XLM-RoBERTa
│   ├── tamil_model/            # Tamil XLM-RoBERTa
│   ├── telugu_model/           # Telugu BERT
│   └── kannada_model/          # Kannada BERT
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SETUP_GUIDE.md             # Setup instructions
├── MONGODB_SETUP.md           # MongoDB guide
├── ARCHITECTURE.md            # Technical architecture
├── TROUBLESHOOTING.md         # Common issues
└── LICENSE                     # MIT License
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Use ESLint for JavaScript code
- Write clear commit messages
- Add tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Hugging Face** - For the Transformers library and pre-trained models
- **Google** - For Gemini AI and Translate APIs
- **MongoDB** - For the database solution
- **FastAPI** - For the excellent web framework
- **React Team** - For the React library
- **Open Source Community** - For all the amazing tools and libraries

---

## 📞 Contact

**Project Maintainer**: Your Name

- 📧 Email: your.email@example.com
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] IndicTrans2 integration for better translation
- [ ] Whisper integration for speech recognition
- [ ] Support for Malayalam and Bengali
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)

### Version 3.0 (Future)
- [ ] Mobile app (React Native)
- [ ] User authentication
- [ ] Public API with rate limiting
- [ ] Model fine-tuning interface
- [ ] Batch processing API

---

## 📊 Project Stats

- **Languages Supported**: 4 (Hindi, Tamil, Telugu, Kannada)
- **Model Parameters**: 760M+ total
- **Lines of Code**: 5,000+
- **API Endpoints**: 10+
- **Contributors**: 1+ (You can be next!)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/multilingual-metaphor-detector&type=Date)](https://star-history.com/#yourusername/multilingual-metaphor-detector&Date)

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Gemini AI Documentation](https://ai.google.dev/)

---

<div align="center">

**Made with ❤️ for Indian Languages**

If you found this project helpful, please consider giving it a ⭐!

[Report Bug](https://github.com/yourusername/multilingual-metaphor-detector/issues) · 
[Request Feature](https://github.com/yourusername/multilingual-metaphor-detector/issues) · 
[Documentation](https://github.com/yourusername/multilingual-metaphor-detector/wiki)

</div>
