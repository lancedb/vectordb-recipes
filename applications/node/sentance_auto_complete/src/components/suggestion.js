import React from "react";
import {LightBulbIcon} from '@heroicons/react/24/outline';

function Suggestion({ suggestions, loader }) {
  return (
    <>
      <h2 className = "text-1xl font-semibold text-center mb-6 text-white flex items-center justify-center">
        Real Time autocomplete suggestions based on factual context
        <LightBulbIcon className="h-6 w-6 text-yellow-500" style={{ marginLeft: '6px' }}/>
      </h2>
      < div className = "h-[75vh] w-full p-5 bg-white rounded shadow-[0_4px_15px_rgba(0,0,0,8)] my-6 suggestion-box" >
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
                {item}
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default Suggestion;
