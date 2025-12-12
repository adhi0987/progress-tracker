import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api from '../api';
import './ProgressStats.css';

export default function ProgressStats() {
    const [stats, setStats] = useState<any[]>([]);
    const [overall, setOverall] = useState(0);
    const[totalPdfs,setTotalPdfs]=useState(0);
    const[completedPdfs,setCompletedPdfs]=useState(0);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await api.get('/progress');
                localStorage.setItem('token', res.data.access_token);
                const total_pdfs = res.data.total_pdfs;
                const completed_pdfs = res.data.completed_pdfs;
                const progress_percentage = res.data.progress_percentage;
                
                setOverall(progress_percentage);    
                setCompletedPdfs(completed_pdfs);
                setTotalPdfs(total_pdfs);
                
                // In a real app, use the `completed_at` timestamp
                const statDataTillLastWeek = [];
                for(let i = 7; i >= 1; i--) {
                    // const CompletedDate = new Date().toISOString().split('T')[0];
                    // date.setDate(new Date().getDate() - i);
                    // const day = date.getDay();
                    const dataObj = new Date();
                    dataObj.setDate(dataObj.getDate() - i);
                    const dateString = dataObj.toISOString().split('T')[0];
                    const dayIndex = dataObj.getDay();
                    let dayName = '';
                    switch(dayIndex) {
                        case 0: dayName = 'Sun'; break;
                        case 1: dayName = 'Mon'; break;
                        case 2: dayName = 'Tue'; break;
                        case 3: dayName = 'Wed'; break;
                        case 4: dayName = 'Thu'; break;
                        case 5: dayName = 'Fri'; break;
                        case 6: dayName = 'Sat'; break;
                    }
                    try
                    {

                        const response = await api.get(`/completed_pdfs_in_particular_day/${dateString}`);
                        localStorage.setItem('token', response.data.access_token);
                        statDataTillLastWeek.push({ 
                            day: dayName, 
                            tasks: response.data.NumberofCompletedPdfs 
                        });
                    }
                    catch(error)
                    {
                        console.error('Error fetching completed PDFs for day:', error);
                        statDataTillLastWeek.push({
                            day: dayName,
                            tasks: 0
                        });
                    }
                    // statDataTillLastWeek.push({ day: dayName, tasks: statDataForDay.data.NumberofCompletedPdfs });
                    // statDataTillLastWeek.push({ day: dayName, tasks: statDataForDay.data.NumberofCompletedPdfs });
                }

                // try
                // {
                //     const response = await api.get(`/completed_pdfs_in_particular_day/${currentFullDate}`);
                //     localStorage.setItem('token', response.data.access_token);
                // }
                // catch(error)
                // {
                //     console.error('Error fetching completed PDFs for today:', error);
                // }
                // let currentDayName = '';
                // switch(currentDay) {    
                //     case 0: currentDayName = 'Sun'; break;
                //     case 1: currentDayName = 'Mon'; break;
                //     case 2: currentDayName = 'Tue'; break;
                //     case 3: currentDayName = 'Wed'; break;
                //     case 4: currentDayName = 'Thu'; break;
                //     case 5: currentDayName = 'Fri'; break;
                //     case 6: currentDayName = 'Sat'; break;
                // }
                // const statDataTillLastWeek = [];
                // for(let i = 1; i <= 7; i++) {
                //     const date = new Date();
                //     date.setDate(currentFullDate.getDate() - i);
                //     const day = date.getDay();
                //     let dayName = '';
                //     switch(day) {
                //         case 0: dayName = 'Sun'; break;
                //         case 1: dayName = 'Mon'; break;
                //         case 2: dayName = 'Tue'; break;
                //         case 3: dayName = 'Wed'; break;
                //         case 4: dayName = 'Thu'; break;
                //         case 5: dayName = 'Fri'; break;
                //         case 6: dayName = 'Sat'; break;
                //     }
                //     const statDataForDay  = await api.get("/completed_pdf_in_particular_day/"+date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate());
                //     statDataTillLastWeek.push({ day: dayName, tasks: statDataForDay.data.count });
                // }
                // const completed = statDataTillLastWeek.find(s => s.day === currentDayName)?.tasks || 0;

                // const statData  = await api.get("/completed_pdf_in_particular_day/"+currentFullDate.getFullYear()+"-"+(currentFullDate.getMonth()+1)+"-"+currentFullDate.getDate());

                
                setStats([...statDataTillLastWeek.reverse()]);
            } catch(e) { console.error(e); }
        };
        fetchStats();
    }, [totalPdfs,completedPdfs,overall]);

    return (
        <div className="progress-stats">
            <div className="statistics">
                <h3>Total PDFS</h3>
                <span>{totalPdfs}</span>
                <h3>Completed PDFs </h3>
                <span>{completedPdfs}</span>
            </div>
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