# Contributing to Multilingual Metaphor Detector

First off, thank you for considering contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)

---

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - Why is this enhancement useful?
- **Proposed solution**
- **Alternative solutions** considered

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues for beginners
- `help wanted` - Issues that need attention

---

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (optional)
- Git

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/multilingual-metaphor-detector.git
cd multilingual-metaphor-detector

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 4. Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY

# 5. Run tests
python -m pytest backend/
cd frontend && npm test

# 6. Start development servers
# Terminal 1
cd backend && uvicorn main:app --reload

# Terminal 2
cd frontend && npm run dev
```

---

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   # Run backend tests
   pytest backend/
   
   # Run frontend tests
   cd frontend && npm test
   
   # Manual testing
   # Test all affected features
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Use a clear title
   - Describe what changed and why
   - Reference related issues
   - Add screenshots if UI changed

### PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged!

---

## Style Guidelines

### Python Code Style

Follow **PEP 8** style guide:

```python
# Good
def detect_language(text: str) -> str:
    """
    Detect the language of input text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Detected language code
    """
    # Implementation
    pass

# Bad
def detectLanguage(text):
    # No docstring, no type hints
    pass
```

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)
- Use type hints
- Write docstrings for functions
- Use meaningful variable names

### JavaScript/React Code Style

Follow **ESLint** configuration:

```javascript
// Good
const handleSubmit = async (e) => {
  e.preventDefault();
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    setResult(data);
  } catch (error) {
    console.error('Error:', error);
  }
};

// Bad
const handleSubmit = async e => {
  e.preventDefault()
  const response = await fetch(url)
  const data = await response.json()
  setResult(data)
}
```

**Key Points:**
- Use 2 spaces for indentation
- Use semicolons
- Use const/let, not var
- Use arrow functions
- Use meaningful component names

### CSS Style

```css
/* Good - BEM naming convention */
.history-modal {
  background: #1a1a2e;
}

.history-modal__header {
  padding: 20px;
}

.history-modal__header--active {
  background: #667eea;
}

/* Bad */
.modal {
  background: #1a1a2e;
}

.header {
  padding: 20px;
}
```

---

## Commit Messages

Follow **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
feat(backend): add Telugu language support

# Bug fix
fix(frontend): resolve history modal close issue

# Documentation
docs(readme): update installation instructions

# Multiple changes
feat(api): add batch prediction endpoint

- Add new /batch-predict endpoint
- Update API documentation
- Add tests for batch processing

Closes #123
```

---

## Testing Guidelines

### Backend Tests

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={"text": "वह आसमान छू रहा है"}
    )
    assert response.status_code == 200
    assert response.json()["language"] == "hindi"
```

### Frontend Tests

```javascript
// App.test.jsx
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Multilingual Metaphor Detector/i);
  expect(titleElement).toBeInTheDocument();
});
```

---

## Documentation

When adding new features, update:

1. **README.md** - Main documentation
2. **API Documentation** - Add endpoint details
3. **Code Comments** - Explain complex logic
4. **Docstrings** - For all functions/classes

---

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Reach out to maintainers

---

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commit history

Thank you for contributing! 🚀
