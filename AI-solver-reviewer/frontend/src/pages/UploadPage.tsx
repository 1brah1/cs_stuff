import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import './UploadPage.css';

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const ext = droppedFile.name.split('.').pop()?.toLowerCase();
      if (ext === 'txt' || ext === 'pdf') {
        setFile(droppedFile);
        setError(null);
      } else {
        setError('Only .txt and .pdf files are supported');
      }
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const ext = selectedFile.name.split('.').pop()?.toLowerCase();
      if (ext === 'txt' || ext === 'pdf') {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Only .txt and .pdf files are supported');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      // Ensure logged in
      await apiService.login();
      
      const document = await apiService.uploadDocument(file);
      navigate(`/review/${document.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file. Please try again.');
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h1>Upload Document for Review</h1>
        <p className="subtitle">Upload a .txt or .pdf file to get AI-powered feedback</p>

        <div
          className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-input"
            accept=".txt,.pdf"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          <label htmlFor="file-input" className="upload-label">
            {file ? (
              <div className="file-info">
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  {(file.size / 1024).toFixed(2)} KB
                </span>
              </div>
            ) : (
              <>
                <div className="upload-icon">📄</div>
                <p>Drag and drop your file here</p>
                <p className="upload-hint">or click to browse</p>
              </>
            )}
          </label>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={!file || isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload & Review'}
        </button>
      </div>
    </div>
  );
};

export default UploadPage;


