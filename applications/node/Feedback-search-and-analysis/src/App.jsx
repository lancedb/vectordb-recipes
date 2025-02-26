// src/App.jsx
import React, { useState } from "react";
import Dropdown from "./components/Dropdown";
import FeedbackForm from "./components/FeedbackForm";
import ResultsPage from "./components/ResultsPage";

const App = () => {
  const [selectedUser, setSelectedUser] = useState("");
  const [showResults, setShowResults] = useState(false); // Toggle between Feedback & Results Page

  return (
    <div className="container mx-auto">
      {!showResults ? (
        <>
        <div className="flex justify-between">
          <h1 className="text-xl font mb-4 pt-4">Select an employee from the dropdown to provide feedback</h1>
          <button 
            className="mt-4 bg-slate-800 text-white p-2 mb-4 rounded-lg hover:cursor-pointer" 
            onClick={() => setShowResults(true)} // Show results page
          >
            View Results
          </button>
        </div>
          <Dropdown selectedUser={selectedUser} setSelectedUser={setSelectedUser} />
          {selectedUser && <FeedbackForm selectedUser={selectedUser} />}
        </>
      ) : (
        <>
          <ResultsPage selectedUser={selectedUser} setShowResults={setShowResults} />
        </>
      )}
    </div>
  );
};

export default App;
