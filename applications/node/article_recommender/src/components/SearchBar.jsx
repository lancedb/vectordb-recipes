import React, { useState, useEffect } from 'react';

const SearchBar = ({ onSearch, externalQuery }) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    if (externalQuery) {
      setQuery(externalQuery);
    }
  }, [externalQuery]);

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSearch} className="bg-white shadow-md rounded-md p-4 flex items-center">
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 border-none focus:outline-none text-gray-700 placeholder-gray-400"
      />
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md ml-4"
      >
        Search
      </button>
    </form>
  );
};

export default SearchBar;
