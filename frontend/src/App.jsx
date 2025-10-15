import { useState } from 'react';
import './App.css';

function App() {
  const [symptoms, setSymptoms] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [view, setView] = useState('checker'); // 'checker' or 'history'

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symptoms.trim()) {
      setError('Please enter your symptoms.');
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/check_symptoms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An error occurred while fetching the results.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchHistory = async () => {
    setView('history');
    setError('');
    setIsLoading(true);
    try {
        const response = await fetch('http://localhost:8000/history');
        if (!response.ok) {
            throw new Error('Failed to fetch history.');
        }
        const data = await response.json();
        // Parse the JSON string in each history item's response
        const parsedHistory = data.map(item => ({
            ...item,
            response: JSON.parse(item.response)
        }));
        setHistory(parsedHistory);
    } catch (err) {
        setError(err.message);
    } finally {
        setIsLoading(false);
    }
  };

  const handleSwitchView = (newView) => {
    setView(newView);
    setResult(null);
    setError('');
    setSymptoms('');
  }


  return (
    <div className="container">
      <header>
        <h1>Healthcare Symptom Checker</h1>
        <nav>
          <button onClick={() => handleSwitchView('checker')} className={view === 'checker' ? 'active' : ''}>Symptom Checker</button>
          <button onClick={fetchHistory} className={view === 'history' ? 'active' : ''}>View History</button>
        </nav>
      </header>

      {view === 'checker' && (
        <main>
          <div className="disclaimer-box">
            <p><strong>Important Disclaimer:</strong> This tool is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.</p>
            <label>
              <input type="checkbox" checked={agreed} onChange={() => setAgreed(!agreed)} />
              I understand and agree.
            </label>
          </div>

          <form onSubmit={handleSubmit}>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="Enter your symptoms here... (e.g., 'high fever, sore throat, and headache')"
              disabled={!agreed || isLoading}
            />
            <button type="submit" disabled={!agreed || isLoading}>
              {isLoading ? 'Analyzing...' : 'Check Symptoms'}
            </button>
          </form>

          {error && <p className="error">{error}</p>}

          {isLoading && <div className="loader"></div>}

          {result && (
            <div className="results">
              <h2>Analysis Results</h2>
              <div className="card">
                <h3>Potential Conditions</h3>
                <ul>
                  {result.potential_conditions.map((condition, index) => (
                    <li key={index}>
                      <strong>{condition.name} ({condition.likelihood})</strong>: {condition.description}
                    </li>
                  ))}
                </ul>
              </div>
              <div className={`card urgency-${result.recommended_next_steps.urgency_level.toLowerCase().replace(/\s+/g, '-')}`}>
                 <h3>Recommended Next Steps</h3>
                 <p><strong>Urgency: {result.recommended_next_steps.urgency_level}</strong></p>
                 <ul>
                    {result.recommended_next_steps.steps.map((step, index) => (
                      <li key={index}>{step}</li>
                    ))}
                 </ul>
              </div>
              <div className="card disclaimer-result">
                <p>{result.safety_disclaimer}</p>
              </div>
            </div>
          )}
        </main>
      )}

      {view === 'history' && (
        <main className="history-view">
            <h2>Query History</h2>
            {isLoading && <div className="loader"></div>}
            {error && <p className="error">{error}</p>}
            {!isLoading && !error && history.length === 0 && <p>No history found.</p>}
            {!isLoading && !error && history.map(item => (
                    <div key={item.id} className="history-item card">
                        <p><strong>Symptoms:</strong> {item.symptoms}</p>
                        <p><strong>Conditions Suggested:</strong> {item.response.potential_conditions.map(c => c.name).join(', ')}</p>
                        <p><strong>Urgency:</strong> {item.response.recommended_next_steps.urgency_level}</p>
                        <small>Checked on: {new Date(item.created_at).toLocaleString()}</small>
                    </div>
                ))
            }
        </main>
      )}
    </div>
  );
}

export default App;
