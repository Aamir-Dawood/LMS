import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, Clock, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const EmployeeDashboard = () => {
  const { user } = useAuth();
  const [balances, setBalances] = useState(null);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [balRes, reqRes] = await Promise.all([
        axios.get('/api/accounts/balances/'),
        axios.get('/api/leaves/requests/')
      ]);
      
      const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
      const myBal = balRes.data.find(b => b.employee === storedUser.id) || balRes.data[0];
      setBalances(myBal);
      
      setRequests(reqRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading dashboard...</div>;

  const filteredRequests = requests.filter(r => statusFilter === 'all' || r.status === statusFilter);

  return (
    <div>
      <div className="top-header">
        <h1>My Dashboard</h1>
      </div>

      <div className="card" style={{ marginBottom: '2rem', display: 'flex', gap: '2rem', alignItems: 'center' }}>
        <div style={{ backgroundColor: 'var(--primary-color)', color: 'white', padding: '1.5rem', borderRadius: '50%' }}>
          <User size={48} />
        </div>
        <div>
          <h2 style={{ marginBottom: '0.25rem' }}>{user?.first_name || user?.username}</h2>
          <p style={{ margin: 0 }}>Employee ID: {user?.employee_id || 'N/A'}</p>
          <p style={{ margin: 0 }}>Email: {user?.email || 'N/A'}</p>
        </div>
      </div>

      {balances && (
        <div className="grid grid-cols-3" style={{ marginBottom: '2rem' }}>
          <div className="card">
            <h3>Vacation</h3>
            <div className="dashboard-stats">
              <span className="stat-value">{balances.vacation_days}</span>
              <Calendar size={32} color="var(--primary-color)" />
            </div>
          </div>
          <div className="card">
            <h3>Sick Leave</h3>
            <div className="dashboard-stats">
              <span className="stat-value">{balances.sick_days}</span>
              <Clock size={32} color="var(--primary-color)" />
            </div>
          </div>
          <div className="card">
            <h3>Personal Days</h3>
            <div className="dashboard-stats">
              <span className="stat-value">{balances.personal_days}</span>
              <Calendar size={32} color="var(--primary-color)" />
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>My Leave History</h2>
          <div>
            <select className="form-input" style={{ width: 'auto', padding: '0.5rem 1rem' }} value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Denied</option>
            </select>
          </div>
        </div>
        
        {filteredRequests.length === 0 ? (
          <p>No leave requests found.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Dates</th>
                  <th>Days</th>
                  <th>Reason</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredRequests.map(req => (
                  <tr key={req.id}>
                    <td style={{ textTransform: 'capitalize' }}>{req.leave_type}</td>
                    <td>{req.start_date} to {req.end_date}</td>
                    <td>{req.days_requested}</td>
                    <td>{req.reason}</td>
                    <td>
                      <span className={`badge badge-${req.status}`}>{req.status}</span>
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

export default EmployeeDashboard;
