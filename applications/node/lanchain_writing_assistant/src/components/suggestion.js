import React from "react";
import {LightBulbIcon} from '@heroicons/react/24/outline'; // For solid version

function Suggestion({ suggestions, loader }) {
  return (
    <>
      <h2 className = "text-1xl font-semibold text-center mb-6 text-blue-500 flex items-center justify-center">
        Real Time Contextual Insights and factual Suggestions for You
        <LightBulbIcon className="h-6 w-6 text-yellow-500" style={{ marginLeft: '6px' }}/>
      </h2>
      < div className = "h-[75vh] w-full rounded-lg border-2 border-gray-300 my-6 p-6 bg-white shadow-lg transition-shadow hover:shadow-2xl suggestion-box" >
        {loader ? (
          <div role="status" className="max-w-sm animate-pulse">
            <div className="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
            <span className="sr-only">Loading...</span>
          </div>
        ) : (
          <ul className="list-disc pl-5">
            {suggestions.map((item, index) => (
              <li key={index} className="mb-2">
                {item.pageContent}
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default Suggestion;
