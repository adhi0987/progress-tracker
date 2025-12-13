import { useState, useEffect } from 'react';
import { FileText, Upload, CheckSquare, Square, Eye, Trash } from 'lucide-react';
import api from '../api';
import './PDFManager.css';

// const BASE_URL = import.meta.env.VITE_BASE_URL || 'http://127.0.0.1:8000';
const BASE_URL = 'http://127.0.0.1:8000';
interface PDFFile {
    id: number;
    filename: string;
    completed: boolean;
}

// Define the Props interface
interface PDFManagerProps {
    onDataChange: () => void;
}

// Accept props in the component
export default function PDFManager({ onDataChange }: PDFManagerProps) {
    const [pdfs, setPdfs] = useState<PDFFile[]>([]);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        fetchPdfs();
    }, []);

    const fetchPdfs = async () => {
        try {
            const res = await api.get('/pdfs');
            localStorage.setItem('token', res.data.access_token);
            setPdfs(res.data.PdfList);
        } catch (err) {
            console.error(err);
        }
    };

    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files?.[0]) return;
        setUploading(true);
        const formData = new FormData();
        formData.append('file', e.target.files[0]);

        try {
            const response = await api.post('/upload_pdf', formData);
            localStorage.setItem('token', response.data.access_token);
            fetchPdfs();
            onDataChange(); // TRIGGER UPDATE
        } catch (err) {
            console.error("Upload failed");
        } finally {
            setUploading(false);
        }
    };

    const toggleComplete = async (id: number) => {
        try {
            const response = await api.put(`/pdfs/${id}/toggle`);
            localStorage.setItem('token', response.data.access_token);  
            fetchPdfs();
            onDataChange(); // TRIGGER UPDATE
        } catch (err) {
            console.error("Failed to update status");
        }
    };

    const viewPdf = (filename: string) => {
        const pdf_url = BASE_URL + `/uploads/${filename}`; 
        window.open(pdf_url, '_blank');
    };

    const deletePdf = async (id: number) => {
        try {
            await api.delete(`/pdfs/${id}`);
            fetchPdfs();
            onDataChange(); // TRIGGER UPDATE
        } catch (err) {
            console.error("Failed to delete PDF");
        }
    };
    
    return (
        <div className="pdf-manager">
            {/* The render code remains the same as your original file... */}
            <div className="pdf-header">
                <h2>Study Materials</h2>
                <label className="upload-btn">
                    <Upload size={18} />
                    {uploading ? 'Uploading...' : 'Upload PDF'}
                    <input type="file" accept="application/pdf" onChange={handleUpload} hidden />
                </label>
            </div>

            <div className="pdf-list">
                {pdfs.length === 0 && <p className="empty-msg">No PDFs uploaded yet.</p>}
                {pdfs.map(pdf => (
                    <div key={pdf.id} className={`pdf-item ${pdf.completed ? 'completed' : ''}`}>
                        <div className="pdf-info">
                            <FileText size={20} />
                            <span>{pdf.filename}</span>
                        </div>
                        <div className="pdf-actions">
                            <button onClick={() => viewPdf(pdf.filename)} title="View">
                                <Eye size={18} />
                            </button>
                            <button onClick={() => toggleComplete(pdf.id)} title="Mark Complete">
                                {pdf.completed ? <CheckSquare color="#4ade80" /> : <Square />}
                            </button>
                            <button onClick={() => deletePdf(pdf.id)} title="Delete">
                                <Trash size={18} />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}