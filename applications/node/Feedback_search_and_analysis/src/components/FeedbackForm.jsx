import React, { useState, useContext } from "react";
import { FeedbackContext } from "../context/FeedBack.context";
import { ThreeDots } from 'react-loader-spinner';

const questions = [
  "Leadership",
  "Creativity",
  "Adaptability",
  "Responsibility",
  "Brand Ambassador",
];
const hoverColors = [
  "hover:bg-red-500", "hover:bg-red-400", "hover:bg-red-300",
  "hover:bg-yellow-300", "hover:bg-yellow-400", "hover:bg-yellow-500",
  "hover:bg-green-300", "hover:bg-green-400", "hover:bg-green-500", "hover:bg-green-600",
];
const scaleColors = [
  "bg-red-500", "bg-red-400", "bg-red-300", "bg-red-200",
  "bg-yellow-200", "bg-yellow-300", "bg-green-200", "bg-green-400",
  "bg-green-500", "bg-green-600",
];

const FeedbackForm = ({ selectedUser }) => {
  const { submitFeedback, loading } = useContext(FeedbackContext);
  const [feedback, setFeedback] = useState({});
  const [comment, setComment] = useState(""); // New state for comments

  const handleSelect = (question, value) => {
    setFeedback({ ...feedback, [question]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const feedbackString = Object.entries(feedback)
      .map(([key, value]) => `${key}: ${value}`)
      .join(", ");
    // Append the comment to the payload
    const finalPayload = comment.trim() ? `${feedbackString}, Comment: ${comment}` : feedbackString;
    
    submitFeedback(selectedUser, finalPayload);
  };

  return (
    <div className="mt-6 p-6 bg-slate-100 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4">Give Feedback</h2>
      {questions.map((question) => (
        <div key={question} className="mb-4">
          <label className="block font-medium mb-2">{question} (1-10):</label>
          <div className="flex space-x-2">
            {[...Array(10)].map((_, index) => {
              const score = index + 1;
              return (
                <button
                  key={score}
                  className={`px-3 py-1 rounded-md text-white font-medium transition-all duration-200 w-10 h-10 ${
                    feedback[question] === score ? scaleColors[index] : "bg-slate-400"
                  } ${hoverColors[index]}`}
                  onClick={() => handleSelect(question, score)}
                >
                  {score}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {/* Comment Section */}
      <div className="mt-4">
        <label className="block font-medium mb-2">Subjective Feedback:</label>
        <textarea
          className="w-full p-2 border border-gray-300 rounded-lg shadow-sm"
          rows="4"
          placeholder="Write your feedback here..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        ></textarea>
      </div>

      <button
        className="bg-slate-800 text-white py-2 px-4 rounded-lg mt-3 hover:bg-slate-600 transition-all duration-200"
        onClick={handleSubmit}
      >
        {loading ? (
          <div className="flex flex-col items-center justify-center flex-1">
            <ThreeDots visible={true} height="20" width="50" color="gray" radius="9" ariaLabel="three-dots-loading" />
          </div>
        ) : (
          <>Submit Feedback</>
        )}
      </button>
    </div>
  );
};

export default FeedbackForm;
