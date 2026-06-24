/**
 * components/MatchInput.jsx — Input form for match analysis queries.
 *
 * Displays:
 * - Text input for natural language query
 * - Submit button with loading state
 * - Example queries for guidance
 */

import React, { useState } from "react";

function MatchInput({ onSubmit, isLoading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query.trim());
    }
  };

  const exampleQueries = [
    "Analyze Arsenal vs Chelsea",
    "Liverpool vs Man United",
    "Man City vs Tottenham",
  ];

  const useExample = (example) => {
    setQuery(example);
  };

  return (
    <div className="match-input">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter match query (e.g., Arsenal vs Chelsea)"
            disabled={isLoading}
            className="match-input-field"
            autoFocus
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="analyze-button"
          >
            {isLoading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      </form>

      <div className="examples">
        <span className="examples-label">Examples:</span>
        {exampleQueries.map((example, index) => (
          <button
            key={index}
            onClick={() => useExample(example)}
            disabled={isLoading}
            className="example-button"
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}

export default MatchInput;
