import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import { CheckCircle, XCircle, Clock, ArrowRight } from 'lucide-react';

const AdminDashboard = () => {
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLeaves();
  }, []);

  const fetchLeaves = async () => {
    try {
      const res = await axios.get('/api/leaves/requests/');
      setLeaves(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading dashboard...</div>;

  const pending = leaves.filter(l => l.status === 'pending');
  const approved = leaves.filter(l => l.status === 'approved');
  const denied = leaves.filter(l => l.status === 'rejected');
  
  // Get latest 5 pending
  const newPendings = [...pending].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 5);

  return (
    <div>
      <div className="top-header">
        <h1>Admin Overview</h1>
      </div>

      <div className="grid grid-cols-3" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3>Pending Requests</h3>
          <div className="dashboard-stats">
            <span className="stat-value" style={{ color: 'var(--warning)' }}>{pending.length}</span>
            <Clock size={32} color="var(--warning)" />
          </div>
        </div>
        <div className="card">
          <h3>Approved Leaves</h3>
          <div className="dashboard-stats">
            <span className="stat-value" style={{ color: 'var(--success)' }}>{approved.length}</span>
            <CheckCircle size={32} color="var(--success)" />
          </div>
        </div>
        <div className="card">
          <h3>Denied Leaves</h3>
          <div className="dashboard-stats">
            <span className="stat-value" style={{ color: 'var(--danger)' }}>{denied.length}</span>
            <XCircle size={32} color="var(--danger)" />
          </div>
        </div>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2>New Pending Requests</h2>
          <button className="btn btn-secondary" onClick={() => navigate('/hr/actions')}>
            View All Actions <ArrowRight size={16} />
          </button>
        </div>
        
        {newPendings.length === 0 ? (
          <p>No new pending requests.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Type</th>
                  <th>Dates</th>
                  <th>Days</th>
                </tr>
              </thead>
              <tbody>
                {newPendings.map(req => (
                  <tr key={req.id} style={{ cursor: 'pointer' }} onClick={() => navigate('/hr/actions')}>
                    <td><strong>{req.employee}</strong></td>
                    <td style={{ textTransform: 'capitalize' }}>{req.leave_type}</td>
                    <td>{req.start_date} to {req.end_date}</td>
                    <td>{req.days_requested}</td>
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

export default AdminDashboard;
