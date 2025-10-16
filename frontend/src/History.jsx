import React, { useState, useEffect } from 'react';
import './History.css';

function History({ apiBaseUrl, onClose }) {
  const [history, setHistory] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState({ language: '', label: '' });
  const [selectedItem, setSelectedItem] = useState(null);

  // Fetch history on component mount
  useEffect(() => {
    fetchHistory();
    fetchStatistics();
  }, [filter]);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const params = new URLSearchParams();
      if (filter.language) params.append('language', filter.language);
      if (filter.label) params.append('label', filter.label);
      
      const response = await fetch(`${apiBaseUrl}/history?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      
      const data = await response.json();
      setHistory(data.history || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching history:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/statistics`);
      if (response.ok) {
        const data = await response.json();
        setStatistics(data.statistics);
      }
    } catch (err) {
      console.error('Error fetching statistics:', err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this prediction?')) {
      return;
    }
    
    try {
      const response = await fetch(`${apiBaseUrl}/history/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error('Failed to delete prediction');
      }
      
      // Refresh history
      fetchHistory();
      fetchStatistics();
      setSelectedItem(null);
    } catch (err) {
      setError(err.message);
      console.error('Error deleting prediction:', err);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to clear all history? This cannot be undone.')) {
      return;
    }
    
    try {
      const response = await fetch(`${apiBaseUrl}/history`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error('Failed to clear history');
      }
      
      // Refresh history
      fetchHistory();
      fetchStatistics();
      setSelectedItem(null);
    } catch (err) {
      setError(err.message);
      console.error('Error clearing history:', err);
    }
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="history-overlay">
      <div className="history-modal">
        <div className="history-header">
          <h2>📜 Prediction History</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        {/* Statistics Section */}
        {statistics && (
          <div className="statistics-section">
            <div className="stat-card">
              <div className="stat-value">{statistics.total_predictions}</div>
              <div className="stat-label">Total Predictions</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{statistics.metaphor_count}</div>
              <div className="stat-label">🎭 Metaphors</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{statistics.normal_count}</div>
              <div className="stat-label">✅ Normal</div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="history-filters">
          <select 
            value={filter.language} 
            onChange={(e) => setFilter({...filter, language: e.target.value})}
            className="filter-select"
          >
            <option value="">All Languages</option>
            <option value="hindi">Hindi</option>
            <option value="tamil">Tamil</option>
            <option value="telugu">Telugu</option>
            <option value="kannada">Kannada</option>
          </select>

          <select 
            value={filter.label} 
            onChange={(e) => setFilter({...filter, label: e.target.value})}
            className="filter-select"
          >
            <option value="">All Types</option>
            <option value="metaphor">Metaphor</option>
            <option value="normal">Normal</option>
          </select>

          <button onClick={fetchHistory} className="refresh-btn">🔄 Refresh</button>
          
          {history.length > 0 && (
            <button onClick={handleClearAll} className="clear-all-btn">🗑️ Clear All</button>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="history-error">
            ⚠️ {error}
          </div>
        )}

        {/* History List */}
        <div className="history-content">
          {isLoading ? (
            <div className="history-loading">
              <div className="loading-spinner"></div>
              <p>Loading history...</p>
            </div>
          ) : history.length === 0 ? (
            <div className="history-empty">
              <p>📭 No predictions in history yet</p>
              <p className="empty-subtitle">Start analyzing text to build your history</p>
            </div>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <div 
                  key={item._id} 
                  className={`history-item ${item.label}`}
                  onClick={() => setSelectedItem(selectedItem?._id === item._id ? null : item)}
                >
                  <div className="history-item-header">
                    <div className="history-item-text">
                      {item.text.length > 80 ? `${item.text.substring(0, 80)}...` : item.text}
                    </div>
                    <div className="history-item-meta">
                      <span className={`badge badge-${item.label}`}>
                        {item.label === 'metaphor' ? '🎭' : '✅'} {item.label}
                      </span>
                      <span className="history-item-lang">{item.language.toUpperCase()}</span>
                    </div>
                  </div>
                  
                  <div className="history-item-footer">
                    <span className="history-item-date">
                      🕐 {formatDate(item.timestamp)}
                    </span>
                    <span className="history-item-confidence">
                      {(item.confidence * 100).toFixed(1)}% confidence
                    </span>
                  </div>

                  {/* Expanded Details */}
                  {selectedItem?._id === item._id && (
                    <div className="history-item-details">
                      <div className="detail-section">
                        <strong>Full Text:</strong>
                        <p>{item.text}</p>
                      </div>
                      
                      {item.translation && (
                        <div className="detail-section">
                          <strong>🌍 Translation:</strong>
                          <p>{item.translation}</p>
                        </div>
                      )}
                      
                      {item.explanation && (
                        <div className="detail-section">
                          <strong>💡 Explanation:</strong>
                          <p>{item.explanation}</p>
                        </div>
                      )}
                      
                      <button 
                        className="delete-item-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(item._id);
                        }}
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default History;
