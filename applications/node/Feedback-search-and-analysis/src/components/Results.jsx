import React, { useContext } from "react";
import { FeedbackContext } from "../context/FeedBack.context";
import { BatteryWarningVertical} from "phosphor-react";
import { ThreeDots } from 'react-loader-spinner'

const Results = () => {
  const { feedbackData,feedbackAnalysisData,loading,loadAnalysis } = useContext(FeedbackContext);
    if (!feedbackData || feedbackData.length === 0) 
      return <div className="p-6 mt-4 bg-slate-200 shadow-lg flex justify-center rounded-lg h-40 pt-16">
                 <p className="text-slate-800">No feedback available</p>
              </div>;

  const ratingColors = [
    "bg-red-500", "bg-red-400", "bg-orange-400", "bg-orange-300",
    "bg-yellow-400", "bg-yellow-300", "bg-green-300", "bg-green-400",
    "bg-green-500", "bg-green-600"
  ];
const parseFeedback = (feedback) => {
  const keys = ["Leadership", "Creativity", "Adaptability", "Responsibility", "Brand Ambassador", "Comment"];
  const result = {};
  
  let currentKey = null;
  
  feedback.split(", ").forEach((part) => {
    const [key, value] = part.split(": ");

    if (keys.includes(key)) {
      currentKey = key;
      result[currentKey] = value;
    } else {
      // If it's part of a comment, append it
      result[currentKey] += `, ${part}`;
    }
  });

  // Convert numeric values to integers
  for (const key in result) {
    if (key !== "Comment") {
      result[key] = parseInt(result[key], 10);
    }
  }

  return result;
};


  // Function to format the analysis text into readable sections
  const formatAnalysis = (analysisText) => {
    console.log(analysisText.replace("**",""));
    return analysisText.split("\n").map((line, index) => {
      if (line.startsWith("###")) {
        return <h3 key={index} className="text-lg font-bold mt-4">{line.replace("###", "").trim()}</h3>;
      } else if (line.startsWith("1.") || line.startsWith("2.") || line.startsWith("3.") || line.startsWith("4.") || line.startsWith("5.")) {
        return <p key={index} className="mt-2">{line.replace(/\*\*(.*?)\*\*/, "$1")}</p>;
      } else {
        return <p key={index} className="text-gray-700">{line.replace(/\*\*(.*?)\*\*/g, "$1")}</p>;
      }
    });
  };

  return (
    <>
    {loading ? (
        <div className="flex flex-col items-center justify-center flex-1">
                <ThreeDots  visible={true}  height="40" width="80" color="gray" radius="9" ariaLabel="three-dots-loading"/>
              </div>
    ): (<>
        {feedbackAnalysisData === '' && !feedbackData?.length ? (
        <div className="p-6 mt-4 bg-slate-200 shadow-lg flex justify-center rounded-lg h-40 pt-16">
          <p className="text-slate-800">No feedback available</p>
          <BatteryWarningVertical size={24} color="#f40b51" />
        </div>
      ) : (<>
        <div className="p-6 bg-white shadow-lg rounded-lg">
           <h2 className="text-lg font-bold">Employee Analysis</h2>
         {feedbackData.map((entry, index) => {
             const parsedFeedback = parseFeedback(entry.feedback);
        return (
          <div key={entry.userId+index} className="mb-6 p-4 bg-gray-100 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Reviewer {index + 1}</h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(parsedFeedback).map(([category, score]) => (
                <>
                {category === 'Comment' ? (
                  <>
                    <div key={category} className="flex items-center w-full">
                      <span className="font-medium w-40">{category}:</span>
                      <div className={`w-full rounded-full text-stone-600`}>
                        {score}
                      </div>
                    </div>
                  </>
                ) : (
                   <>
                    <div key={category} className="flex items-center">
                      <span className="font-medium w-40">{category}:</span>
                      <div className={`w-10 h-10 flex items-center justify-center text-white font-bold rounded-full ${ratingColors[score - 1]}`}>
                        {score}
                      </div>
                    </div>
                  </> 
                )}
                </>
              ))}
            </div>
          </div>
        );
      })}
      {/* Display Feedback Analysis */}
      <div className="mt-6 p-6 bg-gray-50 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-3">Feedback Analysis</h2>
        {loadAnalysis ? (
          <>
           <div className="flex flex-col items-center justify-center flex-1">
              <ThreeDots  visible={true}  height="40" width="70" color="gray" radius="9" ariaLabel="three-dots-loading"/>
              <span>Analysing the feedbacks of your reviewers</span>
          </div>
          </>
        ): (<>
             {feedbackAnalysisData ? formatAnalysis(feedbackAnalysisData) : <p>No analysis available.</p>}
           </>)}
          </div>
        </div>
        </>
      )}
      </>
    )}
    </>
  );
};

export default Results;



