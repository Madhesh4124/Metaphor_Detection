import React, { useState, useRef } from 'react';
import './App.css';
import VirtualKeyboard from './VirtualKeyboard';
import History from './History';

function App() {
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [translation, setTranslation] = useState('');
  const [speechLang, setSpeechLang] = useState('hi-IN'); // Default to Hindi
  const [showKeyboard, setShowKeyboard] = useState(false);
  const [keyboardLang, setKeyboardLang] = useState('hindi');
  const [showHistory, setShowHistory] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const textareaRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000';

  // Handle text input change
  const handleInputChange = (e) => {
    setInputText(e.target.value);
    setError('');
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter some text or use the microphone');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);
    setTranslation('');

    try {
      // Step 1: Get prediction (now includes translation and explanation)
      const predictionResponse = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!predictionResponse.ok) {
        const errorData = await predictionResponse.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }

      const predictionData = await predictionResponse.json();
      setResult(predictionData);

      // Translation and explanation are now included in the prediction response
      setTranslation(predictionData.translation);
    } catch (err) {
      setError(err.message || 'An error occurred. Please try again later.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle microphone recording using Web Speech API
  const handleMicrophoneClick = async () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      }
    } else {
      // Check if Web Speech API is available
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (!SpeechRecognition) {
        setError('Speech recognition not supported in this browser. Please use Chrome or Edge, or type your text.');
        return;
      }

      try {
        const recognition = new SpeechRecognition();
        mediaRecorderRef.current = recognition;
        
        // Configure recognition for Indian languages
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        // Use selected language for speech recognition
        recognition.lang = speechLang;
        
        recognition.onstart = () => {
          setIsRecording(true);
          setError('');
          console.log('Speech recognition started');
        };

        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          console.log('Recognized text:', transcript);
          setInputText(transcript);
          setIsRecording(false);
        };

        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setIsRecording(false);
          
          if (event.error === 'no-speech') {
            setError('No speech detected. Please try again.');
          } else if (event.error === 'not-allowed') {
            setError('Microphone access denied. Please enable microphone permissions.');
          } else {
            setError('Speech recognition failed. Please type your text instead.');
          }
        };

        recognition.onend = () => {
          setIsRecording(false);
          console.log('Speech recognition ended');
        };

        recognition.start();
        
      } catch (err) {
        console.error('Speech recognition error:', err);
        setError('Speech recognition not available. Please type your text.');
        setIsRecording(false);
      }
    }
  };

  // Handle reset
  const handleReset = () => {
    setInputText('');
    setResult(null);
    setError('');
    setTranslation('');
  };

  // Handle virtual keyboard
  const handleKeyboardToggle = (lang) => {
    setKeyboardLang(lang);
    setShowKeyboard(!showKeyboard);
  };

  const handleVirtualKeyPress = (key) => {
    if (key === 'BACKSPACE') {
      setInputText(prev => prev.slice(0, -1));
    } else {
      setInputText(prev => prev + key);
    }
    
    // Keep focus on textarea
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleCloseKeyboard = () => {
    setShowKeyboard(false);
  };

  // Get result color based on label
  const getResultColor = (label) => {
    return label === 'metaphor' ? 'result-metaphor' : 'result-normal';
  };

  return (
    <div className="app-container">
      <div className="main-card">
        <header className="app-header">
          <div className="header-content">
            <div>
              <h1>🌐 Multilingual Metaphor Detector</h1>
              <p className="subtitle">AI-powered metaphor detection for Hindi, Tamil, Telugu, and Kannada</p>
            </div>
            <button 
              className="history-btn"
              onClick={() => setShowHistory(true)}
              title="View History"
            >
              📜 History
            </button>
          </div>
        </header>

        <form onSubmit={handleSubmit} className="input-section">
          <div className="input-group">
            <textarea
              ref={textareaRef}
              className="text-input"
              placeholder="Enter text in Hindi, Tamil, Telugu, or Kannada..."
              value={inputText}
              onChange={handleInputChange}
              rows="4"
              disabled={isLoading}
            />
            
            <div className="keyboard-selector">
              <label>⌨️ Virtual Keyboard:</label>
              <div className="keyboard-buttons">
                <button
                  type="button"
                  className={`keyboard-btn ${showKeyboard && keyboardLang === 'hindi' ? 'active' : ''}`}
                  onClick={() => handleKeyboardToggle('hindi')}
                  disabled={isLoading}
                >
                  हिंदी
                </button>
                <button
                  type="button"
                  className={`keyboard-btn ${showKeyboard && keyboardLang === 'tamil' ? 'active' : ''}`}
                  onClick={() => handleKeyboardToggle('tamil')}
                  disabled={isLoading}
                >
                  தமிழ்
                </button>
                <button
                  type="button"
                  className={`keyboard-btn ${showKeyboard && keyboardLang === 'telugu' ? 'active' : ''}`}
                  onClick={() => handleKeyboardToggle('telugu')}
                  disabled={isLoading}
                >
                  తెలుగు
                </button>
                <button
                  type="button"
                  className={`keyboard-btn ${showKeyboard && keyboardLang === 'kannada' ? 'active' : ''}`}
                  onClick={() => handleKeyboardToggle('kannada')}
                  disabled={isLoading}
                >
                  ಕನ್ನಡ
                </button>
              </div>
            </div>
            
            <div className="speech-lang-selector">
              <label htmlFor="speech-lang">🎤 Speech Language:</label>
              <select 
                id="speech-lang"
                value={speechLang} 
                onChange={(e) => setSpeechLang(e.target.value)}
                disabled={isLoading || isRecording}
              >
                <option value="hi-IN">Hindi (हिंदी)</option>
                <option value="ta-IN">Tamil (தமிழ்)</option>
                <option value="te-IN">Telugu (తెలుగు)</option>
                <option value="kn-IN">Kannada (ಕನ್ನಡ)</option>
              </select>
            </div>
            
            <div className="button-group">
              <button
                type="button"
                className={`mic-button ${isRecording ? 'recording' : ''}`}
                onClick={handleMicrophoneClick}
                disabled={isLoading}
                title={isRecording ? 'Stop recording' : 'Start recording'}
              >
                {isRecording ? '⏹️ Stop' : '🎤 Record'}
              </button>
              
              <button
                type="submit"
                className="submit-button"
                disabled={isLoading || !inputText.trim()}
              >
                {isLoading ? (
                  <>
                    <span className="loading-spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  '🔍 Analyze'
                )}
              </button>
              
              <button
                type="button"
                className="reset-button"
                onClick={handleReset}
                disabled={isLoading}
              >
                🔄 Reset
              </button>
            </div>
          </div>

          {isRecording && (
            <div className="recording-indicator">
              <span className="recording-dot"></span>
              Recording... Click "Stop" when done
            </div>
          )}

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}
        </form>

        {result && (
          <div className={`result-section ${getResultColor(result.label)}`}>
            <h2>📊 Analysis Results</h2>
            
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">Language:</span>
                <span className="result-value">{result.language.toUpperCase()}</span>
              </div>
              
              <div className="result-item">
                <span className="result-label">Classification:</span>
                <span className={`result-value badge ${result.label === 'metaphor' ? 'badge-metaphor' : 'badge-normal'}`}>
                  {result.label === 'metaphor' ? '🎭 Metaphor' : '✅ Normal'}
                </span>
              </div>
              
              <div className="result-item">
                <span className="result-label">Confidence:</span>
                <span className="result-value">{(result.confidence * 100).toFixed(2)}%</span>
              </div>
            </div>

            <div className="result-text">
              <strong>Input Text:</strong>
              <p>{result.text}</p>
            </div>

            {translation && (
              <div className="translation-section">
                <h3>🌍 English Translation</h3>
                <p className="translation-text">{translation}</p>
              </div>
            )}

            {result.explanation && (
              <div className="explanation-section">
                <h3>💡 Metaphor Explanation</h3>
                <p className="explanation-text">{result.explanation}</p>
              </div>
            )}
          </div>
        )}

        <footer className="app-footer">
          <p>Supports Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), and Kannada (ಕನ್ನಡ)</p>
        </footer>
      </div>

      {/* Virtual Keyboard */}
      {showKeyboard && (
        <VirtualKeyboard
          language={keyboardLang}
          onKeyPress={handleVirtualKeyPress}
          onClose={handleCloseKeyboard}
        />
      )}

      {/* History Modal */}
      {showHistory && (
        <History
          apiBaseUrl={API_BASE_URL}
          onClose={() => setShowHistory(false)}
        />
      )}
    </div>
  );
}

export default App;
