import React, { useState } from 'react';
import axios from 'axios'; // Import Axios for making API calls

const SearchBar = ({ handleSearchResults }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Make API request to fetch search results based on the searchQuery
    try {
      const response = await axios.get(`http://localhost:5000/search?query=${encodeURIComponent(searchQuery)}`);
      handleSearchResults(response.data); // Pass the search results to the parent component
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={searchQuery}
        onChange={handleChange}
        placeholder="Enter your search query..."
      />
      <button type="submit">Search</button>
    </form>
  );
};

export default SearchBar;
