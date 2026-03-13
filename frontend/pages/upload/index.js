import { useState } from 'react';
import { useRouter } from 'next/router';

import { useAuth } from '../../components/AuthProvider';
import Layout from '../../components/Layout';
import Loader from '../../components/Loader';
import ProtectedRoute from '../../components/ProtectedRoute';
import api from '../../lib/api';

export default function UploadPage() {
  const router = useRouter();
  const { token } = useAuth();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setError('Choose a CSV export before submitting.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      setIsUploading(true);
      setError('');
      setMessage('');

      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });

      setMessage(`${response.data.recordsInserted} rows processed successfully.`);
      router.push('/dashboard');
    } catch (uploadError) {
      setError(uploadError.response?.data?.detail || 'Upload failed.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <ProtectedRoute>
      <Layout title="Upload CSV Export">
        <section className="card-grid">
          <article className="hero-card">
            <p className="eyebrow">Upload Flow</p>
            <h2>Send your MyFitnessPal export to the FastAPI ingestion endpoint.</h2>
            <p className="lead">
              The backend validates the schema, normalizes dates and macros, and writes cleaned rows into PostgreSQL for Grafana.
            </p>
            <form className="upload-form" onSubmit={handleSubmit}>
              <label className="file-dropzone" htmlFor="csv-upload">
                <span>Choose MyFitnessPal CSV</span>
                <input
                  id="csv-upload"
                  type="file"
                  accept=".csv,text/csv"
                  onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
                />
                <strong>{selectedFile ? selectedFile.name : 'No file selected yet'}</strong>
              </label>
              <button type="submit" className="primary-button" disabled={isUploading}>
                {isUploading ? 'Processing export...' : 'Upload and Process'}
              </button>
            </form>
            {message && <p className="success-text">{message}</p>}
            {error && <p className="error-text">{error}</p>}
          </article>

          <aside className="info-card">
            <h3>Expected columns</h3>
            <ul>
              <li>Date</li>
              <li>Meal</li>
              <li>Food</li>
              <li>Calories</li>
              <li>Carbs</li>
              <li>Protein</li>
              <li>Fat</li>
            </ul>
          </aside>
        </section>
        {isUploading && <Loader label="Cleaning CSV data and inserting records..." />}
      </Layout>
    </ProtectedRoute>
  );
}
