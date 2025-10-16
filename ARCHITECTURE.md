# 🏗️ System Architecture

Visual guide to understanding how the Multilingual Metaphor Detection system works.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   FRONTEND (React)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Text Input / Speech Recording                     │   │
│  │  • Language Detection Display                        │   │
│  │  • Results Visualization                             │   │
│  │  • Error Handling                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                    Port: 3000                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API Calls
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                      │   │
│  │  • /predict    - Metaphor detection                 │   │
│  │  • /translate  - Translation                        │   │
│  │  • /speech     - Speech-to-text                     │   │
│  │  • /health     - Health check                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                    Port: 8000                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Model Inference
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   ML MODELS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Hindi Model  │  │ Tamil Model  │  │Kannada Model │     │
│  │ XLM-RoBERTa  │  │ XLM-RoBERTa  │  │Kannada-BERT  │     │
│  │   270M       │  │   270M       │  │   110M       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### 1. User Input Flow

```
User Types Text
      │
      ▼
┌─────────────┐
│ Text Input  │
│   Field     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Submit    │
│   Button    │
└─────┬───────┘
      │
      ▼
┌─────────────────────┐
│  Frontend Validation│
│  • Check not empty  │
│  • Trim whitespace  │
└─────┬───────────────┘
      │
      ▼
┌─────────────────────┐
│  API Request        │
│  POST /predict      │
│  { text: "..." }    │
└─────┬───────────────┘
      │
      ▼
   Backend
```

### 2. Backend Processing Flow

```
API Request Received
      │
      ▼
┌──────────────────┐
│ Language         │
│ Detection        │
│ • Unicode check  │
│ • Keyword match  │
└────┬─────────────┘
     │
     ├─── Hindi ────┐
     ├─── Tamil ────┤
     └─── Kannada ──┤
                    │
                    ▼
         ┌──────────────────┐
         │ Load Appropriate │
         │     Model        │
         └────┬─────────────┘
              │
              ▼
         ┌──────────────────┐
         │   Tokenization   │
         │ • Convert to IDs │
         │ • Add padding    │
         └────┬─────────────┘
              │
              ▼
         ┌──────────────────┐
         │ Model Inference  │
         │ • Forward pass   │
         │ • Get logits     │
         └────┬─────────────┘
              │
              ▼
         ┌──────────────────┐
         │   Softmax        │
         │ • Calculate prob │
         │ • Get confidence │
         └────┬─────────────┘
              │
              ▼
         ┌──────────────────┐
         │ Classification   │
         │ • Metaphor (1)   │
         │ • Normal (0)     │
         └────┬─────────────┘
              │
              ▼
         ┌──────────────────┐
         │  JSON Response   │
         │ {                │
         │   language: "hi" │
         │   label: "..."   │
         │   confidence: #  │
         │ }                │
         └────┬─────────────┘
              │
              ▼
         Frontend Display
```

### 3. Translation Flow (If Metaphor Detected)

```
Metaphor Detected
      │
      ▼
┌─────────────────┐
│ Frontend checks │
│ label == "meta" │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ POST /translate │
│ {               │
│   text: "..."   │
│   source: "hi"  │
│ }               │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Backend         │
│ Translation     │
│ (IndicTrans2)   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Display English │
│ Translation     │
└─────────────────┘
```

---

## 🧩 Component Architecture

### Frontend Components

```
App.jsx (Main Component)
│
├── State Management
│   ├── inputText
│   ├── isRecording
│   ├── isLoading
│   ├── result
│   ├── error
│   └── translation
│
├── Input Section
│   ├── Text Area
│   ├── Record Button
│   ├── Analyze Button
│   └── Reset Button
│
├── Results Section
│   ├── Language Display
│   ├── Label Badge (Metaphor/Normal)
│   ├── Confidence Score
│   └── Translation (if applicable)
│
└── Error Handling
    └── Error Message Display
```

### Backend Structure

```
main.py (FastAPI App)
│
├── Configuration
│   ├── CORS Middleware
│   ├── Logging Setup
│   └── Model Paths
│
├── Global State
│   ├── models = {}
│   └── tokenizers = {}
│
├── Utility Functions
│   ├── detect_language()
│   └── load_models()
│
├── API Endpoints
│   ├── GET  /health
│   ├── POST /predict
│   ├── POST /translate
│   └── POST /speech
│
└── Startup Event
    └── Load all models
```

---

## 🔐 Data Flow Diagram

```
┌──────────┐
│  Input   │
│  "वह..." │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ Language Detection  │
│ Result: "hindi"     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Model Selection     │
│ Load: hindi_model   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Tokenization        │
│ [101, 45, 67, ...]  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Model Forward Pass  │
│ Logits: [0.2, 0.8]  │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Softmax             │
│ Probs: [0.1, 0.9]   │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ Classification      │
│ Label: "metaphor"   │
│ Confidence: 0.9     │
└────┬────────────────┘
     │
     ▼
┌─────────────────────┐
│ JSON Response       │
│ {                   │
│   language: "hindi" │
│   label: "metaphor" │
│   confidence: 0.9   │
│ }                   │
└─────────────────────┘
```

---

## 🎨 UI State Diagram

```
┌─────────────┐
│   Initial   │
│   State     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  User Types │
│    Text     │
└──────┬──────┘
       │
       ▼
┌─────────────┐     No      ┌─────────────┐
│  Text Empty?├─────────────▶│  Enable     │
└──────┬──────┘              │  Submit Btn │
       │ Yes                 └─────────────┘
       ▼
┌─────────────┐
│  Disable    │
│  Submit Btn │
└─────────────┘

User Clicks Submit
       │
       ▼
┌─────────────┐
│  isLoading  │
│  = true     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Disable    │
│  All Inputs │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  API Call   │
└──────┬──────┘
       │
       ├─── Success ───┐
       │               ▼
       │        ┌─────────────┐
       │        │  Display    │
       │        │  Results    │
       │        └─────────────┘
       │
       └─── Error ─────┐
                       ▼
                ┌─────────────┐
                │  Display    │
                │  Error Msg  │
                └─────────────┘
```

---

## 🔄 Model Loading Sequence

```
Application Startup
       │
       ▼
┌──────────────────┐
│ @app.on_event    │
│ ("startup")      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ load_models()    │
└────┬─────────────┘
     │
     ├─── For each language ───┐
     │                          │
     │                          ▼
     │                   ┌──────────────┐
     │                   │ Check path   │
     │                   │ exists       │
     │                   └──┬───────────┘
     │                      │
     │                      ▼
     │                   ┌──────────────┐
     │                   │ Load         │
     │                   │ Tokenizer    │
     │                   └──┬───────────┘
     │                      │
     │                      ▼
     │                   ┌──────────────┐
     │                   │ Load Model   │
     │                   └──┬───────────┘
     │                      │
     │                      ▼
     │                   ┌──────────────┐
     │                   │ Set to eval  │
     │                   │ mode         │
     │                   └──┬───────────┘
     │                      │
     │                      ▼
     │                   ┌──────────────┐
     │                   │ Store in     │
     │                   │ global dict  │
     │                   └──────────────┘
     │
     ▼
┌──────────────────┐
│ All Models Ready │
│ Server Running   │
└──────────────────┘
```

---

## 🌐 Network Communication

```
Frontend (Port 3000)          Backend (Port 8000)
       │                             │
       │  HTTP POST /predict         │
       ├────────────────────────────▶│
       │  Content-Type: JSON         │
       │  { text: "..." }            │
       │                             │
       │                             ├─ Process
       │                             ├─ Detect Language
       │                             ├─ Run Model
       │                             └─ Generate Response
       │                             │
       │  HTTP 200 OK                │
       │◀────────────────────────────┤
       │  Content-Type: JSON         │
       │  {                          │
       │    language: "hindi",       │
       │    label: "metaphor",       │
       │    confidence: 0.92         │
       │  }                          │
       │                             │
       │  HTTP POST /translate       │
       ├────────────────────────────▶│
       │  { text: "...",             │
       │    source_language: "hi" }  │
       │                             │
       │  HTTP 200 OK                │
       │◀────────────────────────────┤
       │  {                          │
       │    translated_text: "..."   │
       │  }                          │
       │                             │
```

---

## 📦 File Structure with Responsibilities

```
project_root/
│
├── backend/
│   ├── main.py
│   │   ├── FastAPI app initialization
│   │   ├── CORS configuration
│   │   ├── Model loading logic
│   │   ├── Language detection
│   │   ├── API endpoints
│   │   └── Error handling
│   │
│   └── test_api.py
│       └── Automated API testing
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   │   ├── Main component
│   │   │   ├── State management
│   │   │   ├── API communication
│   │   │   ├── Event handlers
│   │   │   └── UI rendering
│   │   │
│   │   ├── App.css
│   │   │   ├── Component styling
│   │   │   ├── Responsive design
│   │   │   ├── Animations
│   │   │   └── Color schemes
│   │   │
│   │   ├── main.jsx
│   │   │   └── React entry point
│   │   │
│   │   └── index.css
│   │       └── Global styles
│   │
│   ├── index.html
│   │   └── HTML template
│   │
│   ├── package.json
│   │   └── Dependencies
│   │
│   └── vite.config.js
│       └── Build configuration
│
└── models/
    ├── hindi_model/
    │   ├── config.json
    │   ├── tokenizer files
    │   └── model weights
    │
    ├── tamil_model/
    │   └── (same structure)
    │
    └── kannada_model/
        └── (same structure)
```

---

## 🔍 Language Detection Logic

```
Input Text
    │
    ▼
┌─────────────────────┐
│ Check Unicode Range │
└────┬────────────────┘
     │
     ├─── U+0900-097F ──▶ Hindi (Devanagari)
     │
     ├─── U+0B80-0BFF ──▶ Tamil
     │
     ├─── U+0C80-0CFF ──▶ Kannada
     │
     └─── No Match ─────┐
                        │
                        ▼
              ┌─────────────────┐
              │ Keyword Matching│
              └────┬────────────┘
                   │
                   ├─── Hindi keywords found ──▶ Hindi
                   ├─── Tamil keywords found ──▶ Tamil
                   ├─── Kannada keywords found ─▶ Kannada
                   │
                   └─── No Match ──▶ Error: Unsupported Language
```

---

## 🎯 Model Inference Pipeline

```
Input: "वह आसमान छू रहा है"
           │
           ▼
┌──────────────────────┐
│ Tokenizer            │
│ • Split into tokens  │
│ • Convert to IDs     │
│ • Add special tokens │
│   [CLS] ... [SEP]    │
└────┬─────────────────┘
     │
     │ input_ids: [101, 45, 67, 89, 102]
     │ attention_mask: [1, 1, 1, 1, 1]
     │
     ▼
┌──────────────────────┐
│ Model (XLM-RoBERTa)  │
│ • Embedding layer    │
│ • 12 Transformer     │
│   layers             │
│ • Classification     │
│   head               │
└────┬─────────────────┘
     │
     │ logits: [0.2, 0.8]
     │         [normal, metaphor]
     │
     ▼
┌──────────────────────┐
│ Softmax              │
│ exp(x) / sum(exp(x)) │
└────┬─────────────────┘
     │
     │ probabilities: [0.12, 0.88]
     │
     ▼
┌──────────────────────┐
│ ArgMax               │
│ Get highest prob     │
└────┬─────────────────┘
     │
     │ predicted_class: 1 (metaphor)
     │ confidence: 0.88
     │
     ▼
Output: {
  label: "metaphor",
  confidence: 0.88
}
```

---

## 🔄 Error Handling Flow

```
Request Received
      │
      ▼
┌─────────────┐
│ Try Block   │
└──────┬──────┘
       │
       ├─── Success ──▶ Return 200 + Data
       │
       └─── Exception ─┐
                       │
                       ▼
            ┌──────────────────┐
            │ Exception Type?  │
            └────┬─────────────┘
                 │
                 ├─── HTTPException ──▶ Return as-is
                 │
                 ├─── ValueError ─────▶ Return 400 + Message
                 │
                 ├─── FileNotFound ───▶ Return 500 + "Model not found"
                 │
                 └─── Other ──────────▶ Return 500 + Generic message
```

---

## 💾 State Management (Frontend)

```
App Component State
│
├── inputText: string
│   └── User's input text
│
├── isRecording: boolean
│   └── Microphone recording status
│
├── isLoading: boolean
│   └── API request in progress
│
├── result: object | null
│   ├── language: string
│   ├── label: string
│   ├── confidence: number
│   └── text: string
│
├── error: string
│   └── Error message to display
│
└── translation: string
    └── English translation (if metaphor)
```

---

## 🚀 Performance Optimization

```
Optimization Strategy
│
├── Backend
│   ├── Load models once at startup
│   ├── Keep models in memory
│   ├── Use eval() mode (no gradients)
│   └── Process single requests
│
└── Frontend
    ├── Debounce input validation
    ├── Lazy load components
    ├── Minimize re-renders
    └── Cache API responses (optional)
```

---

## 🔐 Security Considerations

```
Security Measures
│
├── Backend
│   ├── CORS configuration
│   ├── Input validation
│   ├── Rate limiting (to implement)
│   └── Error message sanitization
│
└── Frontend
    ├── XSS prevention (React auto-escapes)
    ├── HTTPS for microphone access
    └── Input sanitization
```

---

This architecture document provides a visual understanding of how all components work together. Use it as a reference when explaining your project!

