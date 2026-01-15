import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService, Document } from '../services/api';
import './HistoryPage.css';

const HistoryPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const navigate = useNavigate();

  const limit = 20;

  useEffect(() => {
    loadDocuments();
  }, [page]);

  const loadDocuments = async () => {
    setIsLoading(true);
    setError(null);

    try {
      await apiService.login();
      const docs = await apiService.getDocuments(page * limit, limit);
      if (page === 0) {
        setDocuments(docs);
      } else {
        setDocuments((prev) => [...prev, ...docs]);
      }
      setHasMore(docs.length === limit);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load documents');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDocumentClick = (documentId: number) => {
    navigate(`/review/${documentId}`);
  };

  const handleLoadMore = () => {
    setPage((prev) => prev + 1);
  };

  if (isLoading && documents.length === 0) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <h1>Document History</h1>

      {error && <div className="error-message">{error}</div>}

      {documents.length === 0 ? (
        <div className="no-documents">
          <p>No documents yet. Upload your first document to get started!</p>
          <button
            className="upload-link-button"
            onClick={() => navigate('/')}
          >
            Go to Upload
          </button>
        </div>
      ) : (
        <>
          <div className="documents-list">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="document-card"
                onClick={() => handleDocumentClick(doc.id)}
              >
                <div className="document-info">
                  <h3 className="document-name">{doc.filename}</h3>
                  <p className="document-meta">
                    {doc.file_type.toUpperCase()} •{' '}
                    {new Date(doc.created_at).toLocaleDateString()} •{' '}
                    {doc.review_count} review{doc.review_count !== 1 ? 's' : ''}
                  </p>
                </div>
                <div className="document-arrow">→</div>
              </div>
            ))}
          </div>

          {hasMore && (
            <div className="load-more-container">
              <button
                className="load-more-button"
                onClick={handleLoadMore}
                disabled={isLoading}
              >
                {isLoading ? 'Loading...' : 'Load More'}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HistoryPage;





