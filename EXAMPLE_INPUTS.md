# 📝 Example Test Inputs

Use these examples to test your Multilingual Metaphor Detection application.

## 🇮🇳 Hindi Examples

### Metaphorical Expressions

1. **वह आसमान छू रहा है**
   - Translation: "He is touching the sky"
   - Meaning: Achieving great success
   - Expected: **Metaphor**

2. **उसका दिल पत्थर है**
   - Translation: "His heart is stone"
   - Meaning: He is heartless/cruel
   - Expected: **Metaphor**

3. **समय सोना है**
   - Translation: "Time is gold"
   - Meaning: Time is precious
   - Expected: **Metaphor**

4. **वह आग में घी डाल रहा है**
   - Translation: "He is adding ghee to fire"
   - Meaning: Making a bad situation worse
   - Expected: **Metaphor**

5. **उसकी आँखें खुल गईं**
   - Translation: "His eyes opened"
   - Meaning: He realized the truth
   - Expected: **Metaphor** (context-dependent)

### Normal Sentences

1. **मैं स्कूल जा रहा हूं**
   - Translation: "I am going to school"
   - Expected: **Normal**

2. **वह किताब पढ़ रहा है**
   - Translation: "He is reading a book"
   - Expected: **Normal**

3. **आज मौसम अच्छा है**
   - Translation: "The weather is good today"
   - Expected: **Normal**

4. **मुझे खाना पसंद है**
   - Translation: "I like food"
   - Expected: **Normal**

5. **वह दिल्ली में रहता है**
   - Translation: "He lives in Delhi"
   - Expected: **Normal**

---

## 🇮🇳 Tamil Examples

### Metaphorical Expressions

1. **அவன் வானத்தை தொடுகிறான்**
   - Translation: "He is touching the sky"
   - Meaning: Achieving great heights
   - Expected: **Metaphor**

2. **அவள் இதயம் கல்**
   - Translation: "Her heart is stone"
   - Meaning: She is heartless
   - Expected: **Metaphor**

3. **நேரம் பொன்**
   - Translation: "Time is gold"
   - Meaning: Time is precious
   - Expected: **Metaphor**

4. **அவன் நெருப்பில் எண்ணெய் ஊற்றுகிறான்**
   - Translation: "He is pouring oil on fire"
   - Meaning: Making things worse
   - Expected: **Metaphor**

5. **அவன் கண்கள் திறந்தன**
   - Translation: "His eyes opened"
   - Meaning: He understood/realized
   - Expected: **Metaphor** (context-dependent)

### Normal Sentences

1. **நான் பள்ளிக்கு செல்கிறேன்**
   - Translation: "I am going to school"
   - Expected: **Normal**

2. **அவன் புத்தகம் படிக்கிறான்**
   - Translation: "He is reading a book"
   - Expected: **Normal**

3. **இன்று வானிலை நன்றாக உள்ளது**
   - Translation: "The weather is good today"
   - Expected: **Normal**

4. **எனக்கு உணவு பிடிக்கும்**
   - Translation: "I like food"
   - Expected: **Normal**

5. **அவன் சென்னையில் வசிக்கிறான்**
   - Translation: "He lives in Chennai"
   - Expected: **Normal**

---

## 🇮🇳 Kannada Examples

### Metaphorical Expressions

1. **ಅವನು ಆಕಾಶವನ್ನು ಮುಟ್ಟುತ್ತಿದ್ದಾನೆ**
   - Translation: "He is touching the sky"
   - Meaning: Achieving great success
   - Expected: **Metaphor**

2. **ಅವಳ ಹೃದಯ ಕಲ್ಲು**
   - Translation: "Her heart is stone"
   - Meaning: She is heartless
   - Expected: **Metaphor**

3. **ಸಮಯ ಚಿನ್ನ**
   - Translation: "Time is gold"
   - Meaning: Time is precious
   - Expected: **Metaphor**

4. **ಅವನು ಬೆಂಕಿಯಂತೆ ಕೋಪಗೊಂಡನು**
   - Translation: "He became angry like fire"
   - Meaning: Became very angry
   - Expected: **Metaphor**

5. **ಅವನ ಕಣ್ಣುಗಳು ತೆರೆದವು**
   - Translation: "His eyes opened"
   - Meaning: He realized/understood
   - Expected: **Metaphor** (context-dependent)

### Normal Sentences

1. **ನಾನು ಶಾಲೆಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ**
   - Translation: "I am going to school"
   - Expected: **Normal**

2. **ಅವನು ಪುಸ್ತಕ ಓದುತ್ತಿದ್ದಾನೆ**
   - Translation: "He is reading a book"
   - Expected: **Normal**

3. **ಇಂದು ಹವಾಮಾನ ಚೆನ್ನಾಗಿದೆ**
   - Translation: "The weather is good today"
   - Expected: **Normal**

4. **ನನಗೆ ಆಹಾರ ಇಷ್ಟ**
   - Translation: "I like food"
   - Expected: **Normal**

5. **ಅವನು ಬೆಂಗಳೂರಿನಲ್ಲಿ ವಾಸಿಸುತ್ತಾನೆ**
   - Translation: "He lives in Bangalore"
   - Expected: **Normal**

---

## 🎯 Testing Strategy

### For Demonstration:

1. **Start with a clear metaphor** (e.g., "वह आसमान छू रहा है")
   - Shows the system works
   - Easy to explain the metaphorical meaning

2. **Show a normal sentence** (e.g., "मैं स्कूल जा रहा हूं")
   - Demonstrates the system can distinguish
   - Shows the green vs blue color coding

3. **Try a different language** (e.g., Tamil or Kannada)
   - Proves multilingual capability
   - Shows automatic language detection

4. **Show confidence scores**
   - Explain what the percentage means
   - Discuss model reliability

### For Testing:

1. **Test each language separately**
   - Verify all three models load correctly
   - Check language detection accuracy

2. **Test edge cases**
   - Very short sentences
   - Mixed language text (should show error)
   - Empty input (should show error)

3. **Test UI responsiveness**
   - Try on different screen sizes
   - Test all buttons (Record, Analyze, Reset)

4. **Test error handling**
   - Stop backend and try to analyze
   - Enter English text (unsupported language)

---

## 📊 Expected Confidence Scores

- **High Confidence (>85%)**: Clear metaphors or obviously normal sentences
- **Medium Confidence (70-85%)**: Context-dependent expressions
- **Low Confidence (<70%)**: Ambiguous sentences (may need more context)

---

## 🎓 Tips for Presentation

### Good Examples to Show:

1. **Hindi Metaphor**: "वह आसमान छू रहा है" - Very clear, easy to explain
2. **Tamil Normal**: "நான் பள்ளிக்கு செல்கிறேன்" - Simple, straightforward
3. **Kannada Metaphor**: "ಅವನು ಬೆಂಕಿಯಂತೆ ಕೋಪಗೊಂಡನು" - Vivid imagery

### Examples to Avoid During Demo:

1. Very long sentences (takes time to type)
2. Ambiguous expressions (hard to explain)
3. Sentences with typos (may confuse the model)

### Backup Examples (if something fails):

Keep 2-3 tested examples ready that you **know** work correctly. Test these before your presentation.

---

## 🔬 Advanced Testing

### Test Language Detection:

```python
# Hindi (Devanagari script): U+0900 to U+097F
# Tamil script: U+0B80 to U+0BFF
# Kannada script: U+0C80 to U+0CFF
```

### Test Model Accuracy:

Create a spreadsheet with:
- Input text
- Expected label
- Actual label
- Confidence score
- Correct? (Yes/No)

Calculate accuracy: (Correct predictions / Total predictions) × 100

---

## 📝 Copy-Paste Ready Examples

For quick testing, here are one-liners you can copy:

**Hindi Metaphor**: `वह आसमान छू रहा है`

**Hindi Normal**: `मैं स्कूल जा रहा हूं`

**Tamil Metaphor**: `அவன் வானத்தை தொடுகிறான்`

**Tamil Normal**: `நான் பள்ளிக்கு செல்கிறேன்`

**Kannada Metaphor**: `ಅವನು ಬೆಂಕಿಯಂತೆ ಕೋಪಗೊಂಡನು`

**Kannada Normal**: `ನಾನು ಶಾಲೆಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ`

---

**Happy Testing! 🚀**
