import React from 'react';

const PillBar = ({ onCategoryClick }) => {
  const categories = ['Global war', 'climate', 'economy', 'india', 'environment', 'finance'];

  return (
    <div className="flex justify-center space-x-4 mt-4">
      {categories.map((category, index) => (
        <button
          key={index}
          className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-full"
          onClick={() => onCategoryClick(category)}
        >
          {category}
        </button>
      ))}
    </div>
  );
};

export default PillBar;
