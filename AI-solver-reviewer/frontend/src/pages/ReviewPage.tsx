import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService, Review } from '../services/api';
import './ReviewPage.css';
import ReactMarkdown from 'react-markdown';

const ReviewPage: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>();
  const navigate = useNavigate();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReviews();
  }, [documentId]);

  const loadReviews = async () => {
    if (!documentId) return;

    setIsLoading(true);
    setError(null);

    try {
      await apiService.login();
      const loadedReviews = await apiService.getReviews(parseInt(documentId));
      setReviews(loadedReviews);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load reviews');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReview = async () => {
    if (!documentId) return;

    setIsGenerating(true);
    setError(null);

    try {
      await apiService.login();
      await apiService.createReview(parseInt(documentId));
      await loadReviews();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate review');
    } finally {
      setIsGenerating(false);
    }
  };



  if (isLoading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="review-page">
      <div className="review-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Upload
        </button>
        <h1>Document Reviews</h1>
        <button
          className="generate-button"
          onClick={handleGenerateReview}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating Review...' : 'Generate New Review'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {reviews.length === 0 ? (
        <div className="no-reviews">
          <p>No reviews yet. Click "Generate New Review" to get AI feedback.</p>
        </div>
      ) : (
        <div className="reviews-list">
          {reviews.map((review) => (
            <div key={review.id} className="review-card">
              <div className="review-header-info">
                <span className="review-date">
                  {new Date(review.created_at).toLocaleString()}
                </span>
                <span className={`review-status ${review.status}`}>
                  {review.status}
                </span>
              </div>
              <div className="review-content">
                <ReactMarkdown>{review.review_text}</ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReviewPage;






