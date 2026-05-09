import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Check, X } from 'lucide-react';

const AdminActions = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      // HR Manager endpoint for pending leaves
      const res = await axios.get('/api/leaves/requests/');
      const pendingOnly = res.data.filter(r => r.status === 'pending');
      setRequests(pendingOnly);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDecision = async (id, action) => {
    try {
      await axios.post(`/api/leaves/requests/${id}/decision/`, { action, comments: `Processed by Admin/HR` });
      // Refresh list
      fetchRequests();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to process request');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="top-header">
        <h1>Pending Actions</h1>
      </div>
      
      <div className="card">
        {requests.length === 0 ? (
          <p>No pending leave requests require your action.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Type</th>
                  <th>Reason</th>
                  <th>Dates</th>
                  <th>Days</th>
                  <th style={{ textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {requests.map(req => (
                  <tr key={req.id}>
                    <td><strong>{req.employee}</strong></td>
                    <td style={{ textTransform: 'capitalize' }}>{req.leave_type}</td>
                    <td>{req.reason}</td>
                    <td>{req.start_date} <br/>to<br/> {req.end_date}</td>
                    <td>{req.days_requested}</td>
                    <td style={{ textAlign: 'right' }}>
                      <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                        <button className="btn btn-success" onClick={() => handleDecision(req.id, 'approve')}>
                          <Check size={16} /> Approve
                        </button>
                        <button className="btn btn-danger" onClick={() => handleDecision(req.id, 'reject')}>
                          <X size={16} /> Deny
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminActions;
