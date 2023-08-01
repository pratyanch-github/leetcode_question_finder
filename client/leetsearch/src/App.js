import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar.js';
import SearchResults from './components/SearchResults.js';

function App() {
  const [searchResults, setSearchResults] = useState({});

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  return (
    <div className="App">
      <h1>LeetSearch</h1>
      <SearchBar handleSearchResults={handleSearchResults} />
      <SearchResults results={searchResults} />
    </div>
  );
}

export default App;
