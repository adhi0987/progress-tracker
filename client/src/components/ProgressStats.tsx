import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api from '../api';
import './ProgressStats.css';

export default function ProgressStats() {
    const [stats, setStats] = useState<any[]>([]);
    const [overall, setOverall] = useState(0);
    const [totalPdfs, setTotalPdfs] = useState(0);
    const [completedPdfs, setCompletedPdfs] = useState(0);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // 1. Fetch Overall Stats
                const res = await api.get('/progress');
                // Note: The backend rotates tokens, so saving it is fine, 
                // but ensure this doesn't cause race conditions in other components.
                localStorage.setItem('token', res.data.access_token);
                
                setOverall(res.data.progress_percentage);    
                setCompletedPdfs(res.data.completed_pdfs);
                setTotalPdfs(res.data.total_pdfs);
                
                // 2. Prepare dates for the last 7 days
                const datePromises = [];
                // Loop to generate dates (e.g., T-7 to T-1)
                // If you want to include "Today", start i at 0.
                for(let i = 6; i >= 0; i--) {
                    const dataObj = new Date();
                    dataObj.setDate(dataObj.getDate() - i);
                    
                    const dateString = dataObj.toISOString().split('T')[0];
                    const dayIndex = dataObj.getDay();
                    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                    const dayName = dayNames[dayIndex];

                    // Create a promise for each request
                    datePromises.push(
                        api.get(`/completed_pdfs_in_particular_day/${dateString}`)
                           .then(response => ({
                               day: dayName,
                               tasks: response.data.NumberofCompletedPdfs
                           }))
                           .catch(err => {
                               console.error(`Error fetching for ${dateString}`, err);
                               return { day: dayName, tasks: 0 };
                           })
                    );
                }

                // 3. Run all requests in parallel
                const results = await Promise.all(datePromises);
                
                // 4. Update state (No .reverse() needed if we want Oldest -> Newest)
                setStats(results);

            } catch(e) { 
                console.error(e); 
            }
        };

        fetchStats();
        // dependency array is empty to run only once on mount
    }, []); 

    return (
        <div className="progress-stats">
            <div className="statistics">
                <div className="stat-item">
                    <h3>Total PDFs</h3>
                    <span>{totalPdfs}</span>
                </div>
                <div className="stat-item">
                    <h3>Completed</h3>
                    <span>{completedPdfs}</span>
                </div>
            </div>
            <div className="overall-progress">
                <h3>Overall Completion</h3>
                <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${overall}%` }}></div>
                </div>
                <span>{overall.toFixed(1)}%</span>
            </div>
            
            <div className="chart-container">
                <h3>Daily Activity (Last 7 Days)</h3>
                <div style={{ width: '100%', height: 200 }}>
                    <ResponsiveContainer>
                        <BarChart data={stats}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                            <XAxis dataKey="day" stroke="#888" />
                            <YAxis stroke="#888" allowDecimals={false} />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#333', border: 'none', color: '#fff' }} 
                                cursor={{fill: 'rgba(255,255,255,0.1)'}}
                            />
                            <Bar dataKey="tasks" fill="#646cff" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}