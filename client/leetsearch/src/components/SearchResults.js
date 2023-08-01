import React from 'react';

const SearchResults = ({ results }) => {
  if (!results || typeof results !== 'object' || Object.keys(results).length === 0) {
    // If results is not defined, not an object, or an empty object, display a message or return null.
    return <div>No results found.</div>;
  }

  return (
    <div>
      <h2>Search Results</h2>
      <ul>
        {Object.keys(results).map((question, index) => (
          <li key={index}>
            <a href={results[question]} target="_blank" rel="noopener noreferrer">
              {question}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchResults;
