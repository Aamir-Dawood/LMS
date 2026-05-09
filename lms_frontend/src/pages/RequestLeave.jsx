import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RequestLeave = () => {
  const [formData, setFormData] = useState({ leave_type: 'vacation', start_date: '', end_date: '', reason: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/api/leaves/requests/', formData);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit request');
    }
  };

  return (
    <div>
      <div className="top-header">
        <h1>Request Leave</h1>
      </div>

      <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
        {error && (
          <div style={{ padding: '0.75rem', backgroundColor: '#FEE2E2', color: '#DC2626', borderRadius: '8px', marginBottom: '1rem' }}>
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="grid grid-cols-2">
          <div className="form-group" style={{ gridColumn: '1 / -1' }}>
            <label className="form-label">Type of Leave</label>
            <select 
              className="form-input" 
              value={formData.leave_type} 
              onChange={e => setFormData({...formData, leave_type: e.target.value})}
            >
              <option value="vacation">Vacation</option>
              <option value="sick">Sick Leave</option>
              <option value="personal">Personal Leave</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">From Date</label>
            <input type="date" className="form-input" required 
              value={formData.start_date} onChange={e => setFormData({...formData, start_date: e.target.value})} />
          </div>
          <div className="form-group">
            <label className="form-label">To Date</label>
            <input type="date" className="form-input" required 
              value={formData.end_date} onChange={e => setFormData({...formData, end_date: e.target.value})} />
          </div>
          <div className="form-group" style={{ gridColumn: '1 / -1' }}>
            <label className="form-label">Reason</label>
            <textarea className="form-input" required rows="4"
              value={formData.reason} onChange={e => setFormData({...formData, reason: e.target.value})}></textarea>
          </div>
          <div style={{ gridColumn: '1 / -1', display: 'flex', gap: '1rem' }}>
            <button type="button" className="btn btn-secondary" onClick={() => navigate('/')}>Cancel</button>
            <button type="submit" className="btn btn-primary">Submit Request</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RequestLeave;
