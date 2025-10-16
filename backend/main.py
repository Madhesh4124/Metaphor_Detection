from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import torch
import numpy as np
from typing import Optional, List
import logging
from pathlib import Path
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
import hashlib
import time
from database import (
    connect_to_mongodb,
    close_mongodb_connection,
    save_prediction,
    get_prediction_history,
    get_prediction_by_id,
    delete_prediction,
    clear_all_history,
    get_statistics
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multilingual Metaphor Detection API")

# Simple in-memory cache for predictions
prediction_cache = {}
CACHE_TTL = 3600  # 1 hour

def get_cache_key(text: str) -> str:
    """Generate cache key for text"""
    return hashlib.md5(text.encode()).hexdigest()

def get_cached_prediction(text: str) -> Optional[dict]:
    """Get cached prediction if available and not expired"""
    cache_key = get_cache_key(text)
    if cache_key in prediction_cache:
        cached_data = prediction_cache[cache_key]
        if time.time() - cached_data['timestamp'] < CACHE_TTL:
            logger.info(f"Cache hit for text: {text[:50]}...")
            return cached_data['result']
        else:
            # Remove expired cache entry
            del prediction_cache[cache_key]
    return None

def cache_prediction(text: str, result: dict):
    """Cache prediction result"""
    cache_key = get_cache_key(text)
    prediction_cache[cache_key] = {
        'result': result,
        'timestamp': time.time()
    }
    logger.info(f"Cached prediction for text: {text[:50]}...")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
    logger.warning("AI explanations will not work without a valid API key.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("Gemini API configured successfully")
        logger.info(f"API Key starts with: {GEMINI_API_KEY[:10]}...")
    except Exception as e:
        logger.error(f"Failed to configure Gemini API: {str(e)}")
        GEMINI_API_KEY = None

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
models = {}
tokenizers = {}
MODEL_BASE_PATH = Path(__file__).parent.parent / "models"

# Language mapping for our supported languages
LANGUAGE_MAP = {
    'hi': 'hindi',
    'ta': 'tamil',
    'te': 'telugu',
    'kn': 'kannada'
}

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    language: str
    label: str
    confidence: float
    text: str
    translation: str
    explanation: Optional[str] = None

class TranslationRequest(BaseModel):
    text: str
    source_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str

def detect_language(text: str) -> str:
    """
    Detect language using langdetect library
    """
    try:
        # Use langdetect to detect language
        detected_lang = detect(text)
        logger.info(f"LangDetect result: {detected_lang}")

        # Map to our supported languages
        if detected_lang in LANGUAGE_MAP:
            return LANGUAGE_MAP[detected_lang]

        # Fallback to character-based detection for Indic languages
        # Check for Devanagari script (Hindi)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hindi'

        # Check for Tamil script
        if any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'tamil'

        # Check for Telugu script
        if any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'telugu'

        # Check for Kannada script
        if any('\u0C80' <= char <= '\u0CFF' for char in text):
            return 'kannada'

        # Default fallback
        logger.warning(f"Unsupported language detected: {detected_lang}, defaulting to hindi")
        return 'hindi'

    except LangDetectException as e:
        logger.error(f"Language detection failed: {str(e)}")

        # Fallback to character-based detection
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hindi'
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'tamil'
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'telugu'
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):
            return 'kannada'
        else:
            logger.warning("Could not detect language, defaulting to hindi")
            return 'hindi'
    
def generate_metaphor_explanation(text: str, language: str, confidence: float) -> str:
    """
    Generate contextual explanation for detected metaphors using Gemini AI
    """
    # Check if Gemini API is configured
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not configured")
        return "⚠️ AI explanation unavailable - please configure GEMINI_API_KEY in .env file"

    try:
        # Create the Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # Enhanced prompt for accurate metaphor explanations
        prompt = f"""Analyze this {language} metaphor and explain it in simple English.

TEXT: "{text}"

Provide a clear explanation that:
1. Identifies what is being compared to what
2. Explains the deeper meaning or message
3. Is 1-2 sentences maximum
4. Starts with "This metaphor..." or "It compares..."

Example for "Life is a journey":
"This metaphor compares life to a journey, suggesting that life is about the experiences and growth along the way, not just reaching the end goal."

Your explanation (keep it concise and specific to this text):"""

        # Generate the explanation with safety settings
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Lower temperature for more focused responses
                max_output_tokens=100,
            )
        )

        if response and response.text:
            explanation = response.text.strip()

            # Clean up the response
            explanation = explanation.replace('"', '').replace('*', '').strip()
            
            # Remove any "Explanation:" prefix
            if explanation.lower().startswith('explanation:'):
                explanation = explanation[12:].strip()

            # Ensure it's not too long
            if len(explanation) > 250:
                explanation = explanation[:247] + "..."

            logger.info(f"✅ Generated AI explanation: {explanation}")
            return explanation
        else:
            raise Exception("No response from AI")

    except Exception as e:
        logger.error(f"❌ Error generating AI explanation: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        
        # Return error message so user knows to check API key
        return f"⚠️ AI explanation failed: {str(e)[:100]}. Please check your GEMINI_API_KEY in .env file."

def translate_text(text: str, source_language: str) -> str:
    """
    Translate text from source language to English with metaphor context
    Returns translated text or fallback message
    """
    try:
        logger.info(f"Translation request for {source_language}: {text}")
        
        # Manual translations for common metaphorical expressions
        metaphor_translations = {
            'hindi': {
                'दुख की चादर ने उसे ढक लिया था': 'The blanket of sorrow had covered him/her',
                'खुशी का सूरज निकला': 'The sun of happiness rose',
                'गुस्से की आग भड़की': 'The fire of anger flared up',
                'उम्मीद का दीया जला': 'The lamp of hope was lit',
                'प्रेम की नदी बह रही है': 'The river of love is flowing'
            },
            'tamil': {
                'துக்கத்தின் கடல்': 'Ocean of sorrow',
                'மகிழ்ச்சியின் சூரியன்': 'Sun of happiness',
                'கோபத்தின் நெருப்பு': 'Fire of anger'
            },
            'kannada': {
                'ದುಃಖದ ಸಮುದ್ರ': 'Ocean of sorrow',
                'ಸಂತೋಷದ ಸೂರ್ಯ': 'Sun of happiness',
                'ಕೋಪದ ಬೆಂಕಿ': 'Fire of anger'
            }
        }
        
        # Check for manual translations first
        if source_language in metaphor_translations:
            for original, translation in metaphor_translations[source_language].items():
                if original in text:
                    logger.info(f"Using manual metaphor translation: {translation}")
                    return translation
        
        # Try to use googletrans if available
        try:
            from googletrans import Translator
            translator = Translator()
            
            # Map language codes
            lang_map = {
                'hindi': 'hi',
                'tamil': 'ta',
                'kannada': 'kn',
                'telugu': 'te'
            }
            
            source_lang = lang_map.get(source_language, 'auto')
            result = translator.translate(text, src=source_lang, dest='en')
            translated_text = result.text
            
            logger.info(f"Translation successful: {translated_text}")
            return translated_text
            
        except ImportError:
            # Fallback if googletrans not installed
            logger.warning("googletrans not installed, using placeholder")
            return f"[Translation of '{text}' from {source_language} to English. Install 'googletrans==4.0.0-rc1' for automatic translation.]"
        except Exception as trans_error:
            # Fallback if translation fails
            logger.error(f"Translation error: {str(trans_error)}")
            return f"[Translation temporarily unavailable. Original text: '{text}']"
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return f"[Translation failed: {str(e)}]"

def load_models():
    """Load all language models at startup"""
    languages = ['hindi', 'tamil', 'telugu', 'kannada']
    loaded_count = 0
    
    for lang in languages:
        model_path = MODEL_BASE_PATH / f"{lang}_model"
        
        if not model_path.exists():
            logger.warning(f"Model path not found: {model_path}")
            continue
        
        logger.info(f"Loading {lang} model from {model_path}")
        
        try:
            # Load tokenizer with fallback to slow tokenizer
            try:
                tokenizers[lang] = AutoTokenizer.from_pretrained(
                    str(model_path),
                    use_fast=True
                )
                logger.info(f"✓ Loaded fast tokenizer for {lang}")
            except Exception as e:
                logger.warning(f"Fast tokenizer failed for {lang}, trying slow tokenizer")
                tokenizers[lang] = AutoTokenizer.from_pretrained(
                    str(model_path),
                    use_fast=False
                )
                logger.info(f"✓ Loaded slow tokenizer for {lang}")
            
            # Load model
            models[lang] = AutoModelForSequenceClassification.from_pretrained(
                str(model_path),
                num_labels=2
            )
            models[lang].eval()
            loaded_count += 1
            
            logger.info(f"✓ Successfully loaded {lang} model ({loaded_count}/{len(languages)})")
            
        except Exception as e:
            logger.error(f"✗ Failed to load {lang} model: {str(e)}")
            logger.error(f"  Continuing with other models...")
            continue
    
    if loaded_count == 0:
        raise RuntimeError("No models could be loaded. Please check model files.")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"✓ Model loading complete: {loaded_count}/{len(languages)} models loaded")
    logger.info(f"  Available languages: {', '.join(models.keys())}")
    logger.info(f"{'='*60}\n")

@app.on_event("startup")
async def startup_event():
    """
    Load models and connect to database when the application starts
    """
    logger.info("\n" + "="*60)
    logger.info("Starting Multilingual Metaphor Detection API")
    logger.info("="*60 + "\n")
    
    try:
        load_models()
        logger.info("✓ Models loaded successfully\n")
    except Exception as e:
        logger.error(f"✗ Model loading failed: {str(e)}")
        logger.error("Please check that all model files are present in the models/ directory")
    
    # Connect to MongoDB
    try:
        await connect_to_mongodb()
    except Exception as e:
        logger.error(f"✗ MongoDB connection failed: {str(e)}")
        logger.warning("History feature will be disabled")
    
    logger.info("✓ Application startup complete\n")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Close database connection on shutdown
    """
    logger.info("Shutting down application...")
    await close_mongodb_connection()
    logger.info("✓ Application shutdown complete")

@app.get("/health")
async def health_check():
    """
    Health check endpoint with detailed system information
    """
    import psutil
    import torch
    
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # GPU info if available
        gpu_info = {}
        if torch.cuda.is_available():
            gpu_info = {
                "gpu_available": True,
                "gpu_count": torch.cuda.device_count(),
                "gpu_memory_allocated": torch.cuda.memory_allocated() / 1024**3,  # GB
                "gpu_memory_reserved": torch.cuda.memory_reserved() / 1024**3,   # GB
            }
        else:
            gpu_info = {"gpu_available": False}
        
        return {
            "status": "System is running",
            "models_loaded": list(models.keys()),
            "system_metrics": {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_gb": memory.available / 1024**3,
                "memory_total_gb": memory.total / 1024**3
            },
            "gpu_info": gpu_info,
            "gemini_api_configured": GEMINI_API_KEY is not None
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "System is running with limited monitoring",
            "models_loaded": list(models.keys()),
            "error": str(e)
        }

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: TextInput):
    """
    Predict whether the input text contains a metaphor
    """
    try:
        text = input_data.text.strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Input text cannot be empty")
        
        # Check text length
        if len(text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long. Please limit to 1000 characters.")
        
        # Check cache first
        cached_result = get_cached_prediction(text)
        if cached_result:
            return PredictionResponse(**cached_result)
        
        # Detect language
        language = detect_language(text)
        logger.info(f"Detected language: {language}")
        
        # Check if model is loaded
        if language not in models:
            available_models = list(models.keys())
            raise HTTPException(
                status_code=500,
                detail=f"Model for {language} is not available. Supported languages: {', '.join(available_models)}"
            )
        
        # Get model and tokenizer
        model = models[language]
        tokenizer = tokenizers[language]
        
        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Map prediction to label
        label = "metaphor" if predicted_class == 1 else "normal"
        
        logger.info(f"Prediction: {label} (confidence: {confidence:.4f})")
        
        # Always get translation for the input text
        translation = translate_text(text, language)
        
        # Generate explanation if it's a metaphor
        explanation = None
        if label == "metaphor":
            explanation = generate_metaphor_explanation(text, language, confidence)
        
        result_data = {
            "language": language,
            "label": label,
            "confidence": round(confidence, 4),
            "text": text,
            "translation": translation,
            "explanation": explanation
        }
        
        # Cache the result
        cache_prediction(text, result_data)
        
        # Save to database (async, don't wait for it)
        try:
            await save_prediction(result_data.copy())
        except Exception as db_error:
            logger.warning(f"Failed to save to database: {str(db_error)}")
            # Don't fail the request if database save fails
        
        return PredictionResponse(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text from source language to English
    Uses googletrans library for quick translation (free, no API key needed)
    For production, consider IndicTrans2 or Google Cloud Translation API
    """
    try:
        logger.info(f"Translation request for {request.source_language}: {request.text}")
        
        # Try to use googletrans if available
        try:
            from googletrans import Translator
            translator = Translator()
            
            # Map language codes
            lang_map = {
                'hindi': 'hi',
                'tamil': 'ta',
                'kannada': 'kn'
            }
            
            source_lang = lang_map.get(request.source_language, 'auto')
            result = translator.translate(request.text, src=source_lang, dest='en')
            translated_text = result.text
            
            logger.info(f"Translation successful: {translated_text}")
            
        except ImportError:
            # Fallback if googletrans not installed
            logger.warning("googletrans not installed, using placeholder")
            translated_text = f"[Translation of '{request.text}' from {request.source_language} to English. Install 'googletrans==4.0.0-rc1' for automatic translation.]"
        except Exception as trans_error:
            # Fallback if translation fails
            logger.error(f"Translation error: {str(trans_error)}")
            translated_text = f"[Translation temporarily unavailable. Original text: '{request.text}']"
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_language=request.source_language
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/speech")
async def speech_to_text(audio: UploadFile = File(...)):
    """
    Convert speech to text
    Note: This requires additional setup with Whisper or similar speech recognition
    """
    try:
        # Placeholder for speech-to-text
        # You would integrate Whisper or another speech recognition library here
        
        logger.info(f"Received audio file: {audio.filename}")
        
        # For now, return a placeholder response
        return {
            "text": "[Speech recognition would convert audio to text here. Please integrate Whisper or similar library.]",
            "success": False,
            "message": "Speech recognition not yet implemented. Please type your text instead."
        }
        
    except Exception as e:
        logger.error(f"Speech-to-text error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {str(e)}")

@app.get("/models/info")
async def get_model_info():
    """
    Get detailed information about loaded models
    """
    try:
        model_info = {}
        
        for lang, model in models.items():
            try:
                # Get model parameters count
                total_params = sum(p.numel() for p in model.parameters())
                trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
                
                # Get model config if available
                config_info = {}
                if hasattr(model, 'config'):
                    config_info = {
                        "model_type": getattr(model.config, 'model_type', 'unknown'),
                        "hidden_size": getattr(model.config, 'hidden_size', 'unknown'),
                        "num_layers": getattr(model.config, 'num_hidden_layers', 'unknown'),
                        "vocab_size": getattr(model.config, 'vocab_size', 'unknown')
                    }
                
                model_info[lang] = {
                    "total_parameters": total_params,
                    "trainable_parameters": trainable_params,
                    "model_size_mb": total_params * 4 / 1024 / 1024,  # Approximate size in MB
                    "config": config_info,
                    "tokenizer_vocab_size": len(tokenizers[lang]) if lang in tokenizers else 0
                }
            except Exception as e:
                model_info[lang] = {"error": str(e)}
        
        return {
            "models": model_info,
            "total_models": len(models),
            "supported_languages": list(LANGUAGE_MAP.values())
        }
        
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

# ==================== HISTORY ENDPOINTS ====================

@app.get("/history")
async def get_history(
    limit: int = Query(50, ge=1, le=100, description="Number of results to return"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    language: Optional[str] = Query(None, description="Filter by language"),
    label: Optional[str] = Query(None, description="Filter by label (metaphor/normal)")
):
    """
    Get prediction history with optional filters
    """
    try:
        history = await get_prediction_history(limit=limit, skip=skip, language=language, label=label)
        return {
            "success": True,
            "count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.get("/history/{prediction_id}")
async def get_history_item(prediction_id: str):
    """
    Get a specific prediction by ID
    """
    try:
        prediction = await get_prediction_by_id(prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get prediction: {str(e)}")


@app.delete("/history/{prediction_id}")
async def delete_history_item(prediction_id: str):
    """
    Delete a specific prediction from history
    """
    try:
        success = await delete_prediction(prediction_id)
        if not success:
            raise HTTPException(status_code=404, detail="Prediction not found or already deleted")
        return {"success": True, "message": "Prediction deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete prediction: {str(e)}")


@app.delete("/history")
async def clear_history():
    """
    Clear all prediction history
    """
    try:
        count = await clear_all_history()
        return {
            "success": True,
            "message": f"Cleared {count} predictions from history",
            "deleted_count": count
        }
    except Exception as e:
        logger.error(f"Failed to clear history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")


@app.get("/statistics")
async def get_stats():
    """
    Get statistics about predictions
    """
    try:
        stats = await get_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
