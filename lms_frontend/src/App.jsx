import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet, Link, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { 
  LogOut, LayoutDashboard, FileText, CheckCircle, 
  Clock, ShieldAlert, FileClock
} from 'lucide-react';

// Employee Pages
import Login from './pages/Login';
import EmployeeDashboard from './pages/EmployeeDashboard';
import RequestLeave from './pages/RequestLeave';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminActions from './pages/admin/AdminActions';
import AuditLog from './pages/admin/AuditLog';

const ProtectedRoute = ({ children, requiredRole }) => {
  const { user, loading } = useAuth();
  
  if (loading) return null; // or a loading spinner

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole === 'hr' && !user.groups?.includes('HR_Managers') && !user.is_superuser && user.username !== 'hr_manager') {
    return <Navigate to="/" replace />;
  }
  
  return children ? children : <Outlet />;
};

const SidebarLayout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const isAdmin = user?.groups?.includes('HR_Managers') || user?.is_superuser || user?.username === 'hr_manager';

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <ShieldAlert size={28} />
          LMS Portal
        </div>
        
        <nav className="sidebar-nav">
          {isAdmin ? (
            <>
              <Link to="/hr" className={`sidebar-link ${isActive('/hr')}`}>
                <LayoutDashboard size={20} /> Overview
              </Link>
              <Link to="/hr/actions" className={`sidebar-link ${isActive('/hr/actions')}`}>
                <CheckCircle size={20} /> Actions
              </Link>
              <Link to="/hr/audit" className={`sidebar-link ${isActive('/hr/audit')}`}>
                <FileText size={20} /> Audit Log
              </Link>
            </>
          ) : (
            <>
              <Link to="/" className={`sidebar-link ${isActive('/')}`}>
                <LayoutDashboard size={20} /> Dashboard
              </Link>
              <Link to="/request-leave" className={`sidebar-link ${isActive('/request-leave')}`}>
                <FileClock size={20} /> Request Leave
              </Link>
            </>
          )}
        </nav>

        <div className="sidebar-footer">
          <div style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
            Logged in as:<br/>
            <strong>{user?.username}</strong>
          </div>
          <button onClick={logout} className="btn" style={{ width: '100%', backgroundColor: 'rgba(255,255,255,0.1)', color: 'white' }}>
            <LogOut size={16} /> Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route element={<ProtectedRoute />}>
            <Route element={<SidebarLayout />}>
              {/* Employee Routes */}
              <Route path="/" element={<EmployeeDashboard />} />
              <Route path="/request-leave" element={<RequestLeave />} />

              {/* Admin Routes */}
              <Route path="/hr" element={
                <ProtectedRoute requiredRole="hr">
                  <AdminDashboard />
                </ProtectedRoute>
              } />
              <Route path="/hr/actions" element={
                <ProtectedRoute requiredRole="hr">
                  <AdminActions />
                </ProtectedRoute>
              } />
              <Route path="/hr/audit" element={
                <ProtectedRoute requiredRole="hr">
                  <AuditLog />
                </ProtectedRoute>
              } />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
