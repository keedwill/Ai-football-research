/**
 * pages/Home.jsx — Main page for the AI Football Research App.
 *
 * Orchestrates:
 * - MatchInput component for user queries
 * - API calls to backend
 * - ResultDisplay component for analysis results
 * - Loading and error states
 */

import React, { useState } from "react";
import MatchInput from "../components/MatchInput";
import ResultDisplay from "../components/ResultDisplay";
import { analyzeMatch } from "../services/api";

function Home() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (query) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeMatch(query);
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error("Analysis error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <header className="page-header">
        <h1>⚽ AI Football Research System</h1>
        <p className="subtitle">
          Intelligent match analysis powered by AI • Get insights on form,
          stats, and predictions
        </p>
      </header>

      <main className="page-content">
        <MatchInput onSubmit={handleAnalyze} isLoading={isLoading} />

        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Analyzing match data...</p>
          </div>
        )}

        {!isLoading && <ResultDisplay result={result} error={error} />}
      </main>

      {/* <footer className="page-footer">
        <p>Powered by FastAPI • LangChain • React</p>
      </footer> */}
    </div>
  );
}

export default Home;
