import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import api from '../api';
import './ProgressStats.css';

export default function ProgressStats() {
    const [stats, setStats] = useState<any[]>([]);
    const [overall, setOverall] = useState(0);

    useEffect(() => {
        // Since we don't have a dedicated stats endpoint in this simple version, 
        // we'll calculate it from the PDF list on the client side.
        const fetchStats = async () => {
            try {
                const res = await api.get('/pdfs');
                const pdfs = res.data;
                
                // Calculate Overall
                const completed = pdfs.filter((p:any) => p.completed).length;
                const total = pdfs.length;
                setOverall(total === 0 ? 0 : Math.round((completed/total) * 100));

                // Calculate Day-wise stats (Mock logic for demo: Group by dummy days)
                // In a real app, use the `completed_at` timestamp
                const data = [
                    { day: 'Mon', tasks: 2 },
                    { day: 'Tue', tasks: 5 },
                    { day: 'Wed', tasks: 3 },
                    { day: 'Thu', tasks: 4 },
                    { day: 'Fri', tasks: completed }, // Dynamic for demo
                    { day: 'Sat', tasks: 1 },
                    { day: 'Sun', tasks: 0 },
                ];
                setStats(data);
            } catch(e) { console.error(e); }
        };
        fetchStats();
    }, []);

    return (
        <div className="progress-stats">
            <div className="overall-progress">
                <h3>Overall Completion</h3>
                <div className="progress-bar-container">
                    <div className="progress-bar-fill" style={{ width: `${overall}%` }}></div>
                </div>
                <span>{overall}%</span>
            </div>
            
            <div className="chart-container">
                <h3>Daily Activity</h3>
                <div style={{ width: '100%', height: 200 }}>
                    <ResponsiveContainer>
                        <BarChart data={stats}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                            <XAxis dataKey="day" stroke="#888" />
                            <YAxis stroke="#888" />
                            <Tooltip contentStyle={{ backgroundColor: '#333', border: 'none' }} />
                            <Bar dataKey="tasks" fill="#646cff" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}