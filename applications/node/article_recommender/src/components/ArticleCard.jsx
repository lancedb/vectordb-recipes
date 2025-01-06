import React, { useState } from 'react';

const ArticleCard = ({ title, subtitle, date, category, publisher, author, url, content }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleContent = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-4">
        {/* Title with hover and click functionality */}
        <h3
          className="text-lg font-bold text-blue-600 hover:underline hover:cursor-pointer"
          onClick={() => window.open(url, '_blank', 'noopener,noreferrer')}
        >
          {title}
        </h3>
        {/* Content with "Read more" functionality */}
        <p className="text-gray-500 text-sm mt-2">
          {isExpanded ? content : `${content.slice(0, 100)}...`}
          {!isExpanded && (
            <button
              className="text-blue-500 hover:underline ml-1 cursor-pointer"
              onClick={toggleContent}
            >
              Read more
            </button>
          )}
        </p>
        {isExpanded && (
          <button
            className="text-blue-500 hover:underline mt-2"
            onClick={toggleContent}
          >
            Show less
          </button>
        )}
        <p className="text-gray-600 mt-2">{subtitle}</p>
      </div>
      <div className="border-t border-gray-200 flex justify-between items-center p-4">
        <p className="text-gray-500 text-sm">{date}</p>
        <div className="flex flex-col items-end space-y-1">
          {/* Author Name */}
          <p className="text-gray-700 text-xs italic">by {author}</p>
        </div>
      </div>
    </div>
  );
};

export default ArticleCard;
