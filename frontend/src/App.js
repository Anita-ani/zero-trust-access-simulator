import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [accessPolicy, setAccessPolicy] = useState('');
  const [response, setResponse] = useState(null);

  const handlePolicySubmit = async (event) => {
    event.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/policy', {
        policy: accessPolicy,
      }, {
        headers: {
          Authorization: `Bearer YOUR_API_KEY_HERE`,
        },
      });
      setResponse(res.data);
    } catch (error) {
      console.error('Error submitting policy:', error);
      setResponse({ error: 'Failed to submit policy.' });
    }
  };

  return (
    <div className="App">
      <h1>Zero Trust Access Policy Simulator</h1>
      <form onSubmit={handlePolicySubmit}>
        <input
          type="text"
          value={accessPolicy}
          onChange={(e) => setAccessPolicy(e.target.value)}
          placeholder="Enter access policy"
        />
        <button type="submit">Submit Policy</button>
      </form>
      {response && <div className="response">{JSON.stringify(response)}</div>}
    </div>
  );
}

export default App;
