import React, { useState, useContext } from "react";
import Dropdown from "./Dropdown";
import Results from "./Results";
import { FeedbackContext } from "../context/FeedBack.context";
import { ThreeDots } from 'react-loader-spinner'

const ResultsPage = ({setShowResults}) => {
  const [selectedUser, setSelectedUser] = useState("");
  const { fetchResults,loading } = useContext(FeedbackContext);

  return (
    <div className="p-6">
      <div className="flex justify-between">
           <h1 className="text-2xl font-bold">Results Page</h1>
            {/* Back to Feedback button */}
            <button 
                className="mb-3 bg-slate-800 text-white p-2 rounded-lg hover:bg-slate-700 transition-all duration-200 hover:cursor-pointer" 
                onClick={() => setShowResults(false)} // Go back to feedback form
                >
               Back to Feedback
             </button>
     </div>
      <Dropdown selectedUser={selectedUser} setSelectedUser={setSelectedUser} />
      <button className="bg-slate-800 text-white p-2 rounded-lg mt-3" onClick={() => fetchResults(selectedUser)}>
       {loading ? (
        <div className="flex flex-col items-center justify-center flex-1">
          <ThreeDots  visible={true}  height="20" width="50" color="gray" radius="9" ariaLabel="three-dots-loading"/>
        </div>
        ) : (
          <>
              Fetch Results
          </>
        )}
      </button>
      {selectedUser ? (<><Results/></>): (<></>)}
    </div>
  );
};

export default ResultsPage;
