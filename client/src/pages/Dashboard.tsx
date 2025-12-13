import { useState } from 'react'; // Import useState
import Navbar from '../components/Navbar';
import ClockTimer from '../components/ClockTimer';
import PDFManager from '../components/PDFManager';
import ProgressStats from '../components/ProgressStats';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const navigate = useNavigate();
  // State to trigger refreshes in sibling components
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  // Function to increment trigger, causing ProgressStats to re-fetch
  const handleDataChange = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="dashboard">
      <Navbar onLogout={handleLogout} />
      <div className="dashboard-content">
        <div className="section-timer">
          <h2>Practice Timer</h2>
          <ClockTimer />
        </div>
        <div className="section-main">
          <div className="section-progress">
             {/* Pass the trigger state to ProgressStats */}
             <ProgressStats refreshTrigger={refreshTrigger} />
          </div>
          <div className="section-pdf">
            {/* Pass the handler to PDFManager */}
            <PDFManager onDataChange={handleDataChange} />
          </div>
        </div>
      </div>
    </div>
  );
}