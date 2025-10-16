# 📜 History Feature - Quick Guide

## What's New?

Your Multilingual Metaphor Detector now includes a **History Feature** that stores all your predictions in MongoDB!

---

## ✨ Features

### 1. **View Past Predictions**
- See all your previous text analyses
- Organized by date (newest first)
- Click to expand and see full details

### 2. **Filter & Search**
- Filter by language (Hindi, Tamil, Telugu, Kannada)
- Filter by type (Metaphor or Normal)
- Quick refresh button

### 3. **Statistics Dashboard**
- Total predictions count
- Metaphor vs Normal breakdown
- Language usage distribution

### 4. **Manage History**
- Delete individual predictions
- Clear all history at once
- Automatic timestamping

---

## 🚀 Quick Start

### 1. Install MongoDB

**Windows:**
```bash
# Download from: https://www.mongodb.com/try/download/community
# Install and start the service
net start MongoDB
```

**Or use MongoDB Atlas (Cloud - Free):**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string

### 2. Configure Environment

Edit `.env` file:
```bash
# For Local MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=metaphor_detector

# For MongoDB Atlas
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=metaphor_detector
```

### 3. Install Dependencies

```bash
pip install motor pymongo
```

### 4. Start the Application

```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

### 5. Use the History Feature

1. Click **"📜 History"** button in the top-right corner
2. View your predictions
3. Filter, search, and manage your history!

---

## 📊 What Gets Stored?

Each prediction saves:
- **Text**: Original input text
- **Language**: Detected language
- **Label**: Metaphor or Normal
- **Confidence**: Prediction confidence score
- **Translation**: English translation
- **Explanation**: AI-generated explanation (for metaphors)
- **Timestamp**: When the prediction was made

---

## 🎨 UI Features

### Statistics Cards
- **Total Predictions**: Overall count
- **🎭 Metaphors**: Number of metaphors detected
- **✅ Normal**: Number of normal texts

### History List
- Color-coded by type (blue for metaphor, green for normal)
- Shows language badge
- Displays confidence percentage
- Timestamp for each prediction

### Filters
- **All Languages** or specific language
- **All Types** or Metaphor/Normal only
- **Refresh** button to reload
- **Clear All** button to delete everything

---

## 🔌 API Endpoints

### Get History
```bash
curl http://localhost:8000/history?limit=50
```

### Get Statistics
```bash
curl http://localhost:8000/statistics
```

### Delete Prediction
```bash
curl -X DELETE http://localhost:8000/history/{prediction_id}
```

### Clear All
```bash
curl -X DELETE http://localhost:8000/history
```

---

## ⚙️ Technical Details

### Backend
- **Database**: MongoDB with Motor (async driver)
- **Collection**: `predictions`
- **Indexes**: timestamp, language, label
- **Auto-save**: Every prediction is automatically saved

### Frontend
- **Component**: `History.jsx` + `History.css`
- **State Management**: React hooks
- **Real-time**: Fetches latest data on open
- **Responsive**: Works on mobile and desktop

---

## 🔧 Troubleshooting

### History button shows but no data?

**Check MongoDB connection:**
```bash
# In backend logs, look for:
✓ Successfully connected to MongoDB database: metaphor_detector
```

### MongoDB not connecting?

1. **Verify MongoDB is running:**
   ```bash
   mongosh  # Should connect without errors
   ```

2. **Check `.env` configuration:**
   ```bash
   MONGODB_URL=mongodb://localhost:27017
   ```

3. **See detailed guide:**
   - Read `MONGODB_SETUP.md` for step-by-step instructions

### App works but history disabled?

This is normal! The app works without MongoDB:
- Basic prediction functionality continues
- History feature is simply disabled
- No errors, just a warning in logs

---

## 📈 Performance

- **Fast queries**: Indexed for quick retrieval
- **Pagination**: Loads 50 items at a time
- **Efficient**: Async operations don't block predictions
- **Scalable**: Can handle thousands of predictions

---

## 🔒 Privacy & Data

- **Local storage**: If using local MongoDB, data stays on your machine
- **Cloud option**: MongoDB Atlas for cloud storage
- **Delete anytime**: Clear individual or all history
- **No tracking**: Only stores what you analyze

---

## 💡 Tips

1. **Regular cleanup**: Use "Clear All" periodically to keep database small
2. **Use filters**: Find specific predictions quickly
3. **Check statistics**: Track your usage patterns
4. **Backup**: Use `mongodump` to backup your history

---

## 📚 Related Files

- `backend/database.py` - Database operations
- `backend/main.py` - API endpoints (lines 645-733)
- `frontend/src/History.jsx` - History component
- `frontend/src/History.css` - History styles
- `MONGODB_SETUP.md` - Detailed MongoDB setup guide

---

## 🎉 Enjoy Your New Feature!

The history feature makes it easy to:
- Track your learning progress
- Review past analyses
- Build a personal corpus of metaphors
- Analyze usage patterns

Happy analyzing! 🚀
