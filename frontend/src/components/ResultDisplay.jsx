/**
 * components/ResultDisplay.jsx — Display structured match analysis results.
 *
 * Renders:
 * - Summary section
 * - Form analysis
 * - Head-to-head history
 * - League positions
 * - Insights
 * - Final verdict
 */

import React from "react";

function ResultDisplay({ result, error }) {
  if (error) {
    return (
      <div className="result-display error">
        <h3>❌ Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const { analysis } = result;

  return (
    <div className="result-display">
      <div className="result-section summary">
        <h2>📊 Match Analysis</h2>
        <p className="summary-text">{analysis.summary}</p>
      </div>

      <div className="result-grid">
        <div className="result-section">
          <h3>🏃 Recent Form</h3>
          <pre className="result-content">{analysis.form}</pre>
        </div>

        <div className="result-section">
          <h3>📋 League Position</h3>
          <pre className="result-content">{analysis.league_position}</pre>
        </div>
      </div>

      <div className="result-section">
        <h3>⚔️ Head-to-Head Record</h3>
        <pre className="result-content">{analysis.head_to_head}</pre>
      </div>

      <div className="result-section insights">
        <h3>💡 Key Insights</h3>
        <p className="insights-text">{analysis.insights}</p>
      </div>

      <div className="result-section verdict">
        <h3>🎯 Final Verdict</h3>
        <p className="verdict-text">{analysis.final_verdict}</p>
      </div>
    </div>
  );
}

export default ResultDisplay;
