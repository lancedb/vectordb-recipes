// src/context/FeedbackContext.js
import React, { createContext, useState } from "react";
import axios from "axios";

export const FeedbackContext = createContext();

export const FeedbackProvider = ({ children }) => {
  const [feedbackData, setFeedbackData] = useState([]);
  const [feedbackAnalysisData, setFeedbackAnalysisData] = useState('');
  const [loadAnalysis, setLoadAnalysis] = useState(false);
  const [loading, setLoading] = useState(false);

  const submitFeedback = async (userId, feedback) => {
    try {
      setLoading(true);
      await axios.post("http://localhost:5400/api/store-feedback", { userId, feedback });
      setLoading(false);
      alert("Feedback submitted successfully!");
    } catch (error) {
      console.error("Error submitting feedback:", error);
    }
  };

   const fetchResults = async (userId) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5400/api/get-feedback/${userId}`);
      setFeedbackData(response.data.feedback);
      fetchAnalysisResults(userId);
      setLoading(false);
    } catch (error) {
      userId ? '' : alert("select a user first");
      console.error("Error fetching results:", error);
    }
  };

  const fetchAnalysisResults = async (userId) => {
    try {
      setLoadAnalysis(true);
      const response = await axios.get(`http://localhost:5400/api/analyze-feedback/${userId}`);
      setFeedbackAnalysisData(response.data.feedback_analysis);
      setLoadAnalysis(false);
    } catch (error) {
      userId ? '' : alert("select a user first");
      console.error("Error fetching results:", error);
    }
  };

  return (
    <FeedbackContext.Provider value={{ submitFeedback, fetchResults, feedbackData,feedbackAnalysisData,loading,loadAnalysis }}>
      {children}
    </FeedbackContext.Provider>
  );
};
